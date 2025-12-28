"""
受控文件访问视图 - 所有附件访问必须验证权限
"""
from django.http import FileResponse, Http404, HttpResponseForbidden
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import os
import mimetypes

from .models import Attachment, ProjectMember


class SecureFileDownloadView(LoginRequiredMixin, View):
    """
    安全的文件下载视图
    - 必须登录
    - 必须是项目成员
    - 验证 owner 对象的项目权限
    """
    login_url = '/login/'
    
    def get(self, request, attachment_id):
        # 获取附件对象
        attachment = get_object_or_404(Attachment, id=attachment_id)
        
        # 获取附件的所有者对象
        owner = attachment.get_owner()
        if not owner or not hasattr(owner, 'project'):
            return HttpResponseForbidden('附件关联对象不存在或无项目关联')
        
        project = owner.project
        
        # 检查用户是否是项目成员（超级管理员除外）
        if not request.user.is_superuser:
            try:
                ProjectMember.objects.get(project=project, user=request.user)
            except ProjectMember.DoesNotExist:
                return HttpResponseForbidden('您无权访问此文件')
        
        # 检查文件是否存在
        if not attachment.file or not os.path.exists(attachment.file.path):
            raise Http404('文件不存在')
        
        # 判断是否是图片（支持预览）
        content_type, _ = mimetypes.guess_type(attachment.file.name)
        is_image = content_type and content_type.startswith('image/')
        
        # 打开文件并返回
        file_handle = open(attachment.file.path, 'rb')
        response = FileResponse(file_handle, content_type=content_type)
        
        # 图片允许内联显示，其他文件强制下载
        if is_image and request.GET.get('preview') != 'false':
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(attachment.file.name)}"'
        else:
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment.file.name)}"'
        
        return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attachment_info(request, attachment_id):
    """
    获取附件信息（不下载文件）
    用于前端判断文件类型、大小等
    """
    attachment = get_object_or_404(Attachment, id=attachment_id)
    
    # 验证项目权限
    owner = attachment.get_owner()
    if not owner or not hasattr(owner, 'project'):
        return Response({'error': '附件关联对象不存在'}, status=status.HTTP_403_FORBIDDEN)
    
    project = owner.project
    
    if not request.user.is_superuser:
        try:
            ProjectMember.objects.get(project=project, user=request.user)
        except ProjectMember.DoesNotExist:
            return Response({'error': '您无权访问此文件'}, status=status.HTTP_403_FORBIDDEN)
    
    # 返回文件信息
    file_info = {
        'id': attachment.id,
        'filename': os.path.basename(attachment.file.name),
        'size': attachment.file.size if attachment.file else 0,
        'content_type': mimetypes.guess_type(attachment.file.name)[0],
        'uploaded_at': attachment.uploaded_at,
        'uploaded_by': attachment.uploaded_by.username,
        'is_image': mimetypes.guess_type(attachment.file.name)[0] and 
                   mimetypes.guess_type(attachment.file.name)[0].startswith('image/'),
        # 安全的下载 URL
        'download_url': request.build_absolute_uri(f'/api/v1/attachments/{attachment.id}/download/'),
        'preview_url': request.build_absolute_uri(f'/api/v1/attachments/{attachment.id}/download/?preview=true'),
    }
    
    return Response(file_info)
