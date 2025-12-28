#!/bin/bash

# 端口验证脚本

echo "==================================="
echo "  端口状态检查"
echo "==================================="
echo ""

check_port() {
    local port=$1
    local name=$2
    
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "✅ $name (端口 $port): 运行中"
        lsof -Pi :$port -sTCP:LISTEN | grep LISTEN | awk '{print "   进程: " $1 " (PID: " $2 ")"}'
    else
        echo "❌ $name (端口 $port): 未运行"
    fi
}

echo "检查服务状态："
echo ""
check_port 20003 "前端"
check_port 20004 "后端"
echo ""

echo "测试连接："
echo ""

# 测试后端
if curl -s -o /dev/null -w "%{http_code}" http://localhost:20004/api/v1/projects/ | grep -q "200\|401\|403"; then
    echo "✅ 后端 API: 正常响应"
else
    echo "❌ 后端 API: 无响应"
fi

# 测试前端
if curl -s -o /dev/null -w "%{http_code}" http://localhost:20003/ | grep -q "200"; then
    echo "✅ 前端: 正常响应"
else
    echo "❌ 前端: 无响应"
fi

echo ""
echo "访问地址："
echo "  前端: http://localhost:20003"
echo "  后端: http://localhost:20004"
echo "  管理: http://localhost:20004/admin"
echo "  API:  http://localhost:20004/api/v1"
