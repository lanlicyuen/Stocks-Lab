#!/bin/bash

# 停止开发服务器

cd "$(dirname "$0")"

echo "正在停止服务..."

# 停止 tmux 会话
if tmux has-session -t stocks-lab 2>/dev/null; then
    tmux kill-session -t stocks-lab
    echo "✅ tmux 会话已停止"
fi

# 停止后台进程
if [ -f "backend.pid" ]; then
    kill $(cat backend.pid) 2>/dev/null
    rm backend.pid
    echo "✅ 后端已停止"
fi

if [ -f "frontend.pid" ]; then
    kill $(cat frontend.pid) 2>/dev/null
    rm frontend.pid
    echo "✅ 前端已停止"
fi

# 清理端口（以防进程未正常退出）
lsof -ti:20004 | xargs kill -9 2>/dev/null
lsof -ti:20003 | xargs kill -9 2>/dev/null

echo "✅ 所有服务已停止"
