#!/bin/bash

# 前端开发服务器启动脚本
cd "$(dirname "$0")"

echo "==================================="
echo "  启动前端开发服务器（端口 20003）"
echo "==================================="
echo ""

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "首次运行，正在安装依赖..."
    npm install
    echo ""
fi

echo "前端服务器将在以下地址运行："
echo "  http://localhost:20003"
echo ""
echo "API 后端地址："
echo "  http://localhost:20004/api/v1"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

npm run dev
