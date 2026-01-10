"""
自定义权限类 - 确保多端使用时的数据隔离
Web 端与 Flutter App 共用同一套 API，需要严格的用户级权限控制
"""
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    确保用户只能访问自己的资源
    适用于 MarketAccount 模型
    """
    message = "您无权访问此资源"
    
    def has_object_permission(self, request, view, obj):
        # obj 是 MarketAccount 实例
        return obj.owner == request.user


class IsAccountOwner(permissions.BasePermission):
    """
    确保用户只能访问自己账户下的资源
    适用于 Trade, Security, CashAdjustment 等有 account 外键的模型
    """
    message = "您无权访问此账户下的资源"
    
    def has_permission(self, request, view):
        # 对于列表视图，检查query参数中的account是否属于当前用户
        account_id = request.query_params.get('account')
        print(f"DEBUG: has_permission called - account_id={account_id}, user={request.user.username if request.user.is_authenticated else 'anonymous'}")
        
        if account_id:
            try:
                from .models import MarketAccount
                # 确保account_id是整数
                account_id = int(account_id)
                print(f"DEBUG: Looking for account_id={account_id}")
                account = MarketAccount.objects.get(id=account_id, owner=request.user)
                print(f"DEBUG: Account found: {account.name}")
                return True
            except (ValueError, MarketAccount.DoesNotExist) as e:
                print(f"DEBUG: Account not found or invalid: {e}")
                return False
        print("DEBUG: No account_id specified, allowing access")
        return True  # 如果没有指定account，允许访问（会在queryset中过滤）
    
    def has_object_permission(self, request, view, obj):
        # obj 可以是 Trade, Security, CashAdjustment 等
        return obj.account.owner == request.user


class IsTradeOwner(permissions.BasePermission):
    """
    确保用户只能访问自己交易的附件
    适用于 TradeAttachment 模型
    """
    message = "您无权访问此交易的附件"
    
    def has_object_permission(self, request, view, obj):
        # obj 是 TradeAttachment 实例
        return obj.trade.account.owner == request.user


# ===== 以下为废弃的 Project 相关权限（保留以防回退） =====

class ProjectPermission_DEPRECATED(permissions.BasePermission):
    """
    [已废弃] 项目资源级权限
    """
    
    def has_permission(self, request, view):
        return False  # 禁用
    
    def has_object_permission(self, request, view, obj):
        return False  # 禁用

