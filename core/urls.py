from django.urls import path, include
from django.contrib.auth import logout as django_logout
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .viewsets import (
    TradeViewSet, TradeAttachmentViewSet, AuditLogViewSet, SecurityViewSet, 
    MarketAccountViewSet, CashAdjustmentViewSet
)
from .serializers import UserSerializer

# 创建路由器
router = DefaultRouter()
router.register(r'accounts', MarketAccountViewSet, basename='account')
router.register(r'trades', TradeViewSet, basename='trade')
router.register(r'trade-attachments', TradeAttachmentViewSet, basename='trade-attachment')
router.register(r'securities', SecurityViewSet, basename='security')
router.register(r'cash-adjustments', CashAdjustmentViewSet, basename='cash-adjustment')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """获取当前用户信息"""
    user_data = UserSerializer(request.user).data
    user_data['is_superuser'] = request.user.is_superuser
    return Response(user_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def jwt_login(request):
    """JWT 登录 - 移动端使用"""
    from django.contrib.auth import authenticate
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': '用户名和密码不能为空'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response({
            'error': '用户名或密码错误'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # 生成 JWT tokens
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'user': UserSerializer(user).data,
        'tokens': {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """用户登出（Session 方式，Web 端使用）"""
    django_logout(request)
    return Response({
        'success': True,
        'message': '登出成功'
    }, status=status.HTTP_200_OK)


urlpatterns = [
    # 用户相关
    path('me/', me, name='me'),
    
    # JWT 认证（移动端）
    path('auth/login/', jwt_login, name='jwt-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    
    # Session 登出（Web 端）
    path('auth/logout/', logout_view, name='api-logout'),
    
    # RESTful endpoints
    path('', include(router.urls)),
]
