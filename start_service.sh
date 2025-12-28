#!/bin/bash

# 启动 Stocks-Lab 后端服务

cd /home/lanlic/Html-Project/Stocks-Lab

echo "🚀 启动 Stocks-Lab 投资披露平台..."

# 检查端口占用
if lsof -Pi :20004 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  端口 20004 已被占用，正在停止旧进程..."
    lsof -ti:20004 | xargs kill -9 2>/dev/null
    sleep 2
fi

# 激活虚拟环境（如果有）
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ 虚拟环境已激活"
fi

# 应用数据库迁移
echo "📦 应用数据库迁移..."
python manage.py migrate --noinput

# 创建超级用户（如果不存在）
echo "👤 检查测试账户..."
python manage.py shell << EOF
from django.contrib.auth.models import User
from core.models import Project, ProjectMember

# 创建 admin 用户
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
    print('✅ 创建 admin 用户成功')
else:
    admin_user = User.objects.get(username='admin')
    print('✅ admin 用户已存在')

# 创建 viewer 用户
if not User.objects.filter(username='viewer').exists():
    viewer_user = User.objects.create_user('viewer', 'viewer@test.com', 'viewer123')
    print('✅ 创建 viewer 用户成功')
else:
    viewer_user = User.objects.get(username='viewer')
    print('✅ viewer 用户已存在')

# 创建测试项目
if not Project.objects.filter(name='Demo Project').exists():
    project = Project.objects.create(
        name='Demo Project',
        description='这是一个演示项目',
        created_by=admin_user
    )
    ProjectMember.objects.create(project=project, user=admin_user, role='ADMIN')
    ProjectMember.objects.create(project=project, user=viewer_user, role='VIEWER')
    print('✅ 创建测试项目成功')
else:
    print('✅ 测试项目已存在')
EOF

# 收集静态文件
echo "📦 收集静态文件..."
python manage.py collectstatic --noinput --clear

# 启动服务
echo ""
echo "🎉 启动成功！"
echo ""
echo "访问地址："
echo "  📱 前端: http://localhost:20003"
echo "  🔧 后端API: http://localhost:20004/api/v1/"
echo "  🛠️  管理后台: http://localhost:20004/admin/"
echo ""
echo "测试账号："
echo "  👨‍💼 管理员: admin / admin123"
echo "  👁️  观察者: viewer / viewer123"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 启动后端（监听 20004）
python manage.py runserver 0.0.0.0:20004
