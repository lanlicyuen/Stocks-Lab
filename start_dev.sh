#!/bin/bash

# 统一启动脚本：同时启动前后端

cd "$(dirname "$0")"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║           Stocks-Lab 开发环境统一启动                        ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# 检查后端是否已初始化
if [ ! -d "venv" ]; then
    echo "❌ 后端未初始化，请先运行："
    echo "   ./manage.sh setup"
    exit 1
fi

# 检查数据库
if [ ! -f "db.sqlite3" ]; then
    echo "❌ 数据库未创建，请先运行："
    echo "   ./manage.sh migrate"
    exit 1
fi

# 检查前端依赖
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 安装前端依赖..."
    cd frontend && npm install && cd ..
    echo ""
fi

echo "🚀 启动服务..."
echo ""

# 使用 tmux 或 screen 同时启动前后端
if command -v tmux &> /dev/null; then
    echo "使用 tmux 启动（推荐）"
    echo ""
    
    # 创建新的 tmux 会话
    tmux new-session -d -s stocks-lab
    
    # 后端窗口
    tmux rename-window -t stocks-lab:0 'Backend'
    tmux send-keys -t stocks-lab:0 'cd ~/Html-Project/Stocks-Lab && source venv/bin/activate && python manage.py runserver 0.0.0.0:20004' C-m
    
    # 前端窗口
    tmux new-window -t stocks-lab:1 -n 'Frontend'
    tmux send-keys -t stocks-lab:1 'cd ~/Html-Project/Stocks-Lab/frontend && npm run dev' C-m
    
    # 状态窗口
    tmux new-window -t stocks-lab:2 -n 'Status'
    tmux send-keys -t stocks-lab:2 'echo "=== Stocks-Lab 开发环境 ==="' C-m
    tmux send-keys -t stocks-lab:2 'echo ""' C-m
    tmux send-keys -t stocks-lab:2 'echo "前端: http://localhost:20003"' C-m
    tmux send-keys -t stocks-lab:2 'echo "后端: http://localhost:20004"' C-m
    tmux send-keys -t stocks-lab:2 'echo "管理: http://localhost:20004/admin"' C-m
    tmux send-keys -t stocks-lab:2 'echo ""' C-m
    tmux send-keys -t stocks-lab:2 'echo "切换窗口: Ctrl+B + 数字键(0/1/2)"' C-m
    tmux send-keys -t stocks-lab:2 'echo "停止服务: ./stop_dev.sh 或 tmux kill-session -t stocks-lab"' C-m
    
    # 附加到会话
    echo "✅ 服务已启动！"
    echo ""
    echo "访问地址："
    echo "  前端: http://localhost:20003"
    echo "  后端: http://localhost:20004"
    echo "  管理: http://localhost:20004/admin"
    echo ""
    echo "tmux 快捷键："
    echo "  Ctrl+B + 数字键 - 切换窗口"
    echo "  Ctrl+B + D - 分离会话（后台运行）"
    echo "  tmux attach -t stocks-lab - 重新连接"
    echo ""
    
    tmux attach -t stocks-lab
    
else
    echo "⚠️  未找到 tmux，将使用后台进程模式"
    echo ""
    
    # 启动后端
    echo "🔵 启动后端（端口 20004）..."
    source venv/bin/activate
    nohup python manage.py runserver 0.0.0.0:20004 > backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > backend.pid
    
    # 等待后端启动
    sleep 3
    
    # 启动前端
    echo "🟢 启动前端（端口 20003）..."
    cd frontend
    nohup npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../frontend.pid
    cd ..
    
    echo ""
    echo "✅ 服务已启动！"
    echo ""
    echo "访问地址："
    echo "  前端: http://localhost:20003"
    echo "  后端: http://localhost:20004"
    echo "  管理: http://localhost:20004/admin"
    echo ""
    echo "进程ID："
    echo "  后端: $BACKEND_PID"
    echo "  前端: $FRONTEND_PID"
    echo ""
    echo "查看日志："
    echo "  tail -f backend.log"
    echo "  tail -f frontend.log"
    echo ""
    echo "停止服务："
    echo "  ./stop_dev.sh"
    echo ""
fi
