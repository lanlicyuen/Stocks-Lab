#!/usr/bin/env python
"""验证所有数据模型是否正确创建"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stocks_lab.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import (
    Project, ProjectMember, Contribution,
    DailyBalance, Trade, Attachment, AuditLog
)

def verify_models():
    """验证模型是否可用"""
    models = [
        ('Project', Project),
        ('ProjectMember', ProjectMember),
        ('Contribution', Contribution),
        ('DailyBalance', DailyBalance),
        ('Trade', Trade),
        ('Attachment', Attachment),
        ('AuditLog', AuditLog),
    ]
    
    print("=" * 60)
    print("验证 Stocks-Lab 数据模型")
    print("=" * 60)
    
    for name, model in models:
        try:
            count = model.objects.count()
            fields = [f.name for f in model._meta.get_fields()]
            print(f"\n✅ {name}")
            print(f"   记录数: {count}")
            print(f"   字段: {', '.join(fields[:5])}...")
        except Exception as e:
            print(f"\n❌ {name}")
            print(f"   错误: {e}")
    
    print("\n" + "=" * 60)
    print("模型验证完成！")
    print("=" * 60)
    
    # 显示关键字段信息
    print("\n📋 关键特性：")
    print("  • Project: 投资项目主表")
    print("  • ProjectMember: 成员权限管理 (ADMIN/VIEWER)")
    print("  • Contribution: 出资记录")
    print("  • DailyBalance: 日结余 (project+date unique)")
    print("  • Trade: 交易记录 (thesis markdown 必填)")
    print("  • Attachment: 多图附件 (TRADE/BALANCE)")
    print("  • AuditLog: 完整审计日志")

if __name__ == '__main__':
    verify_models()
