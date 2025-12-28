#!/bin/bash

# Stocks-Lab 快速启动脚本
# 适用于首次部署

echo "==================================="
echo "  Stocks-Lab 快速启动向导"
echo "==================================="
echo ""

cd "$(dirname "$0")"

# 检查是否已经初始化
if [ ! -d "venv" ]; then
    echo "步骤 1/5: 初始化项目..."
    ./manage.sh setup
    echo ""
else
    echo "✓ 项目已初始化，跳过此步骤"
    echo ""
fi

# 激活虚拟环境
source venv/bin/activate

# 检查数据库
if [ ! -f "db.sqlite3" ]; then
    echo "步骤 2/5: 创建数据库..."
    ./manage.sh migrate
    echo ""
else
    echo "✓ 数据库已存在，跳过此步骤"
    echo ""
fi

# 检查是否有管理员
echo "步骤 3/5: 检查管理员账户..."
ADMIN_EXISTS=$(python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.filter(is_superuser=True).exists())" 2>/dev/null)

if [ "$ADMIN_EXISTS" != "True" ]; then
    echo "需要创建管理员账户："
    ./manage.sh admin
    echo ""
else
    echo "✓ 管理员账户已存在"
    echo ""
fi

echo "步骤 4/5: 收集静态文件..."
python manage.py collectstatic --noinput --clear 2>/dev/null
echo ""

echo "步骤 5/5: 启动服务器..."
echo ""
echo "==================================="
echo "  启动完成！"
echo "==================================="
echo ""
echo "访问地址："
echo "  前台: http://localhost:8002"
echo "  后台: http://localhost:8002/admin"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

python manage.py runserver 0.0.0.0:8002
