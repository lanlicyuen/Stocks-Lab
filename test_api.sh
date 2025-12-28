#!/bin/bash
# API 快速测试脚本

BASE_URL="http://localhost:20004/api/v1"
COOKIE_FILE="/tmp/stocks-lab-cookies.txt"

echo "🚀 Stocks-Lab API 快速测试"
echo "================================"
echo ""

# 检查服务是否运行
echo "📡 检查后端服务..."
if ! curl -s -o /dev/null -w "%{http_code}" $BASE_URL/projects/ | grep -q "401\|200"; then
    echo "❌ 后端服务未运行"
    echo "   请先启动: ./manage.sh run"
    exit 1
fi
echo "✅ 后端服务运行中"
echo ""

# 测试账户
ADMIN_USER="admin"
ADMIN_PASS="admin123"

echo "🔑 使用 admin 账户登录..."
# 注意：这里需要通过 Django admin 或自定义登录 endpoint
# 简化版本：直接使用测试数据
echo "⚠️  请确保已运行: python test_api_permissions.py"
echo ""

echo "📋 可用的 API Endpoints:"
echo ""
echo "1. 项目管理"
echo "   GET    $BASE_URL/projects/"
echo "   POST   $BASE_URL/projects/"
echo "   GET    $BASE_URL/projects/{id}/"
echo ""

echo "2. 出资记录"
echo "   GET    $BASE_URL/contributions/?project=1"
echo "   POST   $BASE_URL/contributions/"
echo ""

echo "3. 每日结余"
echo "   GET    $BASE_URL/balances/?project=1"
echo "   POST   $BASE_URL/balances/"
echo ""

echo "4. 净值曲线 ⭐"
echo "   GET    $BASE_URL/balance-summary/?project=1"
echo ""

echo "5. 交易记录"
echo "   GET    $BASE_URL/trades/?project=1"
echo "   POST   $BASE_URL/trades/"
echo ""

echo "6. 附件管理"
echo "   GET    $BASE_URL/attachments/?owner_type=TRADE&owner_id=1"
echo "   POST   $BASE_URL/attachments/"
echo ""

echo "================================"
echo "💡 提示："
echo "   - 使用 Django Session 认证"
echo "   - 前端运行在 http://localhost:20003"
echo "   - 查看完整文档: API_DOCUMENTATION.md"
echo ""

echo "🧪 测试命令示例："
echo ""
echo "# 安装 HTTPie (可选)"
echo "pip install httpie"
echo ""
echo "# 测试获取项目列表 (需要先登录)"
echo "http GET $BASE_URL/projects/ --session=stocks-lab"
echo ""
echo "# 测试净值曲线"
echo "http GET $BASE_URL/balance-summary/ project==1 --session=stocks-lab"
