"""
测试数据创建脚本
使用方法: python create_test_data.py
"""
import os
import django
from datetime import date, datetime, timedelta
from decimal import Decimal

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stocks_lab.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Project, ProjectMember, Contribution, DailyBalance, Trade

def create_test_data():
    print("开始创建测试数据...")
    
    # 创建测试用户
    print("\n1. 创建测试用户...")
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✓ 创建管理员: {admin_user.username}")
    else:
        print(f"✓ 管理员已存在: {admin_user.username}")
    
    viewer_user, created = User.objects.get_or_create(
        username='viewer',
        defaults={
            'email': 'viewer@example.com'
        }
    )
    if created:
        viewer_user.set_password('viewer123')
        viewer_user.save()
        print(f"✓ 创建观察者: {viewer_user.username}")
    else:
        print(f"✓ 观察者已存在: {viewer_user.username}")
    
    # 创建测试项目
    print("\n2. 创建测试项目...")
    project, created = Project.objects.get_or_create(
        name='测试投资项目',
        defaults={
            'description': '这是一个用于测试的投资项目，包含完整的交易和结余记录。',
            'created_by': admin_user
        }
    )
    if created:
        print(f"✓ 创建项目: {project.name}")
    else:
        print(f"✓ 项目已存在: {project.name}")
    
    # 添加项目成员
    print("\n3. 添加项目成员...")
    admin_member, created = ProjectMember.objects.get_or_create(
        project=project,
        user=admin_user,
        defaults={'role': 'ADMIN'}
    )
    if created:
        print(f"✓ 添加管理员: {admin_user.username}")
    else:
        print(f"✓ 管理员已是成员: {admin_user.username}")
    
    viewer_member, created = ProjectMember.objects.get_or_create(
        project=project,
        user=viewer_user,
        defaults={'role': 'VIEWER'}
    )
    if created:
        print(f"✓ 添加观察者: {viewer_user.username}")
    else:
        print(f"✓ 观察者已是成员: {viewer_user.username}")
    
    # 创建出资记录
    print("\n4. 创建出资记录...")
    contributions_data = [
        {'user': admin_user, 'amount': Decimal('100000'), 'date': date.today() - timedelta(days=30)},
        {'user': viewer_user, 'amount': Decimal('50000'), 'date': date.today() - timedelta(days=30)},
    ]
    
    for data in contributions_data:
        contribution, created = Contribution.objects.get_or_create(
            project=project,
            user=data['user'],
            contributed_at=data['date'],
            defaults={
                'amount': data['amount'],
                'notes': f"{data['user'].username} 初始出资",
                'created_by': admin_user
            }
        )
        if created:
            print(f"✓ 创建出资记录: {data['user'].username} - ¥{data['amount']}")
    
    # 创建日结余记录
    print("\n5. 创建日结余记录...")
    base_balance = Decimal('150000')
    for i in range(10):
        balance_date = date.today() - timedelta(days=10-i)
        balance_amount = base_balance + Decimal(str(i * 1000))
        
        balance, created = DailyBalance.objects.get_or_create(
            project=project,
            date=balance_date,
            defaults={
                'balance': balance_amount,
                'notes': f'第{i+1}天结余',
                'created_by': admin_user
            }
        )
        if created:
            print(f"✓ 创建日结余: {balance_date} - ¥{balance_amount}")
    
    # 创建交易记录
    print("\n6. 创建交易记录...")
    trades_data = [
        {
            'symbol': '600519',
            'side': 'BUY',
            'quantity': 100,
            'price': Decimal('1850.50'),
            'days_ago': 8,
            'thesis': '# 茅台买入分析\n\n基于以下理由买入：\n- 业绩稳健增长\n- 估值合理\n- 长期看好',
        },
        {
            'symbol': '000858',
            'side': 'BUY',
            'quantity': 200,
            'price': Decimal('45.80'),
            'days_ago': 5,
            'thesis': '# 五粮液买入分析\n\n- 白酒行业龙头\n- 季度业绩超预期\n- 技术面突破',
        },
        {
            'symbol': '600519',
            'side': 'SELL',
            'quantity': 50,
            'price': Decimal('1920.00'),
            'days_ago': 2,
            'thesis': '# 茅台部分止盈\n\n达到目标价位，止盈一半',
            'review': '盈利 3.76%，符合预期',
        },
    ]
    
    for data in trades_data:
        executed_time = datetime.now() - timedelta(days=data['days_ago'])
        
        trade, created = Trade.objects.get_or_create(
            project=project,
            symbol=data['symbol'],
            side=data['side'],
            executed_at=executed_time,
            defaults={
                'quantity': data['quantity'],
                'price': data['price'],
                'thesis': data['thesis'],
                'review': data.get('review', ''),
                'created_by': admin_user
            }
        )
        if created:
            print(f"✓ 创建交易: {data['symbol']} {data['side']} {data['quantity']}@{data['price']}")
    
    print("\n" + "="*50)
    print("测试数据创建完成！")
    print("="*50)
    print("\n登录信息:")
    print("  管理员 - 用户名: admin, 密码: admin123")
    print("  观察者 - 用户名: viewer, 密码: viewer123")
    print("\n访问地址:")
    print("  前台: http://localhost:8002")
    print("  后台: http://localhost:8002/admin")

if __name__ == '__main__':
    create_test_data()
