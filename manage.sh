#!/bin/bash

# Stocks-Lab 管理脚本

cd "$(dirname "$0")"

case "$1" in
    setup)
        echo "=== 初始化项目 ==="
        
        # 创建虚拟环境
        if [ ! -d "venv" ]; then
            echo "创建虚拟环境..."
            python3 -m venv venv
        fi
        
        # 激活虚拟环境
        source venv/bin/activate
        
        # 安装依赖
        echo "安装依赖..."
        pip install -r requirements.txt
        
        # 创建环境文件
        if [ ! -f ".env" ]; then
            echo "创建环境配置文件..."
            cp .env.example .env
            echo "请编辑 .env 文件配置您的环境变量"
        fi
        
        # 创建必要的目录
        mkdir -p media/attachments
        mkdir -p static
        
        echo "初始化完成！"
        ;;
        
    migrate)
        echo "=== 执行数据库迁移 ==="
        source venv/bin/activate
        python manage.py makemigrations
        python manage.py migrate
        ;;
        
    admin)
        echo "=== 创建管理员账户 ==="
        source venv/bin/activate
        python manage.py createsuperuser
        ;;
        
    run)
        echo "=== 启动后端开发服务器（端口 20004）==="
        source venv/bin/activate
        python manage.py runserver 0.0.0.0:20004
        ;;
        
    test)
        echo "=== 运行测试 ==="
        source venv/bin/activate
        python manage.py test
        ;;
        
    shell)
        echo "=== 进入 Django Shell ==="
        source venv/bin/activate
        python manage.py shell
        ;;
        
    static)
        echo "=== 收集静态文件 ==="
        source venv/bin/activate
        python manage.py collectstatic --noinput
        ;;
        
    clean)
        echo "=== 清理项目 ==="
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
        find . -type f -name "*.pyc" -delete
        find . -type f -name "*.pyo" -delete
        echo "清理完成！"
        ;;
        
    backup)
        echo "=== 备份数据库 ==="
        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        cp db.sqlite3 "db.sqlite3.backup.$TIMESTAMP"
        echo "备份已保存到: db.sqlite3.backup.$TIMESTAMP"
        ;;
        
    status)
        echo "=== 系统状态 ==="
        if [ -d "venv" ]; then
            echo "✓ 虚拟环境已创建"
        else
            echo "✗ 虚拟环境未创建"
        fi
        
        if [ -f "db.sqlite3" ]; then
            echo "✓ 数据库已创建"
        else
            echo "✗ 数据库未创建"
        fi
        
        if [ -f ".env" ]; then
            echo "✓ 环境配置已创建"
        else
            echo "✗ 环境配置未创建"
        fi
        ;;
        
    *)
        echo "Stocks-Lab 管理脚本"
        echo ""
        echo "用法: ./manage.sh [命令]"
        echo ""
        echo "可用命令:"
        echo "  setup    - 初始化项目（创建虚拟环境、安装依赖）"
        echo "  migrate  - 执行数据库迁移"
        echo "  admin    - 创建管理员账户"
        echo "  run      - 启动开发服务器（端口 8002）"
        echo "  test     - 运行测试"
        echo "  shell    - 进入 Django Shell"
        echo "  static   - 收集静态文件"
        echo "  clean    - 清理缓存文件"
        echo "  backup   - 备份数据库"
        echo "  status   - 查看系统状态"
        echo ""
        ;;
esac
