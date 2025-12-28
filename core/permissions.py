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

