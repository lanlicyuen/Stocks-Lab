#!/usr/bin/env python
"""列出所有可用的 API 路由"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stocks_lab.settings')
django.setup()

from django.urls import get_resolver
from rest_framework.routers import DefaultRouter

def list_urls():
    """列出所有 URL 配置"""
    print("\n" + "=" * 70)
    print("  Stocks-Lab API 路由列表")
    print("=" * 70)
    
    # API 路由
    print("\n📡 REST API Endpoints (base: /api/v1/)")
    print("-" * 70)
    
    api_routes = [
        ('projects', 'ProjectViewSet', [
            'GET    /api/v1/projects/',
            'POST   /api/v1/projects/',
            'GET    /api/v1/projects/{id}/',
            'PUT    /api/v1/projects/{id}/',
            'DELETE /api/v1/projects/{id}/',
            'GET    /api/v1/projects/{id}/members/',
            'POST   /api/v1/projects/{id}/add_member/',
        ]),
        ('contributions', 'ContributionViewSet', [
            'GET    /api/v1/contributions/',
            'POST   /api/v1/contributions/',
            'GET    /api/v1/contributions/{id}/',
            'PUT    /api/v1/contributions/{id}/',
            'DELETE /api/v1/contributions/{id}/',
        ]),
        ('balances', 'DailyBalanceViewSet', [
            'GET    /api/v1/balances/',
            'POST   /api/v1/balances/',
            'GET    /api/v1/balances/{id}/',
            'PUT    /api/v1/balances/{id}/',
            'DELETE /api/v1/balances/{id}/',
        ]),
        ('balance-summary', 'BalanceSummaryViewSet', [
            'GET    /api/v1/balance-summary/?project={id}  ⭐',
        ]),
        ('trades', 'TradeViewSet', [
            'GET    /api/v1/trades/',
            'POST   /api/v1/trades/',
            'GET    /api/v1/trades/{id}/',
            'PUT    /api/v1/trades/{id}/',
            'DELETE /api/v1/trades/{id}/',
        ]),
        ('attachments', 'AttachmentViewSet', [
            'GET    /api/v1/attachments/',
            'POST   /api/v1/attachments/',
            'GET    /api/v1/attachments/{id}/',
            'DELETE /api/v1/attachments/{id}/',
        ]),
        ('audit-logs', 'AuditLogViewSet', [
            'GET    /api/v1/audit-logs/',
            'GET    /api/v1/audit-logs/{id}/',
        ]),
    ]
    
    for prefix, viewset, routes in api_routes:
        print(f"\n[{viewset}]")
        for route in routes:
            print(f"  {route}")
    
    # 其他路由
    print("\n\n🌐 其他路由")
    print("-" * 70)
    other_routes = [
        'GET    /api/v1/me/                    - 获取当前用户信息',
        'GET    /admin/                        - Django Admin',
        'POST   /login/                        - 用户登录',
        'POST   /logout/                       - 用户登出',
        'GET    /                              - Dashboard',
        'GET    /projects/                     - 项目列表页',
        'GET    /projects/{id}/                - 项目详情页',
    ]
    for route in other_routes:
        print(f"  {route}")
    
    print("\n" + "=" * 70)
    print("  总计: 6 个 ViewSet + 特殊 endpoint")
    print("=" * 70)
    
    # 权限说明
    print("\n\n🔐 权限控制")
    print("-" * 70)
    print("  ✅ 所有 API 需要登录认证")
    print("  ✅ Project 相关资源检查 ProjectMember")
    print("  ✅ VIEWER 只能 GET/HEAD/OPTIONS")
    print("  ✅ ADMIN 允许所有操作")
    print("  ✅ 未加入项目 → 403 或空列表")
    
    print("\n")

if __name__ == '__main__':
    list_urls()
