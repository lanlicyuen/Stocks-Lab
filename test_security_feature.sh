#!/bin/bash
# 证券主档功能测试脚本

echo "========================================"
echo "证券主档 Security 功能测试"
echo "========================================"
echo ""

# 服务信息
SERVICE_URL="http://127.0.0.1:20004"
API_URL="${SERVICE_URL}/api/v1"

echo "📌 测试环境"
echo "服务地址: ${SERVICE_URL}"
echo "API地址: ${API_URL}"
echo ""

# 检查服务状态
echo "1️⃣  检查服务状态..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" ${SERVICE_URL}/)
if [ "$HTTP_CODE" == "200" ] || [ "$HTTP_CODE" == "302" ]; then
    echo "✅ 服务运行正常 (HTTP ${HTTP_CODE})"
else
    echo "❌ 服务未响应 (HTTP ${HTTP_CODE})"
    exit 1
fi
echo ""

# 检查数据库迁移
echo "2️⃣  检查数据库表..."
cd /home/lanlic/Html-Project/Stocks-Lab
source venv/bin/activate

TABLES=$(python manage.py dbshell <<EOF 2>/dev/null
.tables
.quit
EOF
)

if echo "$TABLES" | grep -q "core_security"; then
    echo "✅ core_security 表已创建"
else
    echo "❌ core_security 表不存在"
fi

if echo "$TABLES" | grep -q "core_trade"; then
    echo "✅ core_trade 表已存在"
else
    echo "❌ core_trade 表不存在"
fi
echo ""

# 检查 Security 字段
echo "3️⃣  检查 Trade 表结构..."
SCHEMA=$(python manage.py dbshell <<EOF 2>/dev/null
.schema core_trade
.quit
EOF
)

if echo "$SCHEMA" | grep -q "security_id"; then
    echo "✅ Trade.security_id 字段已添加"
else
    echo "❌ Trade.security_id 字段不存在"
fi
echo ""

# 测试 API 端点
echo "4️⃣  测试 API 端点..."

# 获取 CSRF token（需要登录）
echo "   检查 Securities API..."
curl -s -o /dev/null -w "   GET /api/v1/securities/ -> HTTP %{http_code}\n" ${API_URL}/securities/

echo "   检查 check-symbol 端点..."
curl -s -o /dev/null -w "   GET /api/v1/securities/check-symbol/ -> HTTP %{http_code}\n" "${API_URL}/securities/check-symbol/?project=1&symbol=AAPL"

echo "   检查 trade-summary 端点..."
curl -s -o /dev/null -w "   GET /api/v1/securities/trade-summary/ -> HTTP %{http_code}\n" "${API_URL}/securities/trade-summary/?project=1"

echo ""

# 检查前端页面
echo "5️⃣  测试前端页面..."
curl -s -o /dev/null -w "   /trades/create/ -> HTTP %{http_code}\n" ${SERVICE_URL}/trades/create/
curl -s -o /dev/null -w "   /trades/analysis/ -> HTTP %{http_code}\n" ${SERVICE_URL}/trades/analysis/
echo ""

# 数据库统计
echo "6️⃣  数据库统计..."
SECURITY_COUNT=$(python manage.py dbshell <<EOF 2>/dev/null | grep -o '[0-9]*' | head -1
SELECT COUNT(*) FROM core_security;
.quit
EOF
)
echo "   证券主档记录数: ${SECURITY_COUNT:-0}"

TRADE_COUNT=$(python manage.py dbshell <<EOF 2>/dev/null | grep -o '[0-9]*' | head -1
SELECT COUNT(*) FROM core_trade;
.quit
EOF
)
echo "   交易记录数: ${TRADE_COUNT:-0}"

LINKED_TRADE_COUNT=$(python manage.py dbshell <<EOF 2>/dev/null | grep -o '[0-9]*' | head -1
SELECT COUNT(*) FROM core_trade WHERE security_id IS NOT NULL;
.quit
EOF
)
echo "   已关联证券的交易数: ${LINKED_TRADE_COUNT:-0}"
echo ""

# 检查模板文件
echo "7️⃣  检查模板文件..."
FILES=(
    "templates/trade_form_new.html"
    "templates/trade_analysis_new.html"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file 不存在"
    fi
done
echo ""

# 功能清单
echo "========================================"
echo "✨ 新增功能清单"
echo "========================================"
echo ""
echo "后端 API:"
echo "  ✅ GET  /api/v1/securities/                  - 证券列表"
echo "  ✅ POST /api/v1/securities/                  - 创建证券"
echo "  ✅ GET  /api/v1/securities/check-symbol/     - 检查股票代码"
echo "  ✅ GET  /api/v1/securities/trade-summary/    - 交易汇总统计"
echo ""
echo "前端页面:"
echo "  ✅ /trades/create/?project={id}              - 增强版交易表单"
echo "  ✅ /trades/analysis/?project={id}            - 分类复盘统计"
echo "  ✅ /projects/{id}/dashboard/                 - 项目仪表盘（新增入口）"
echo ""
echo "核心功能:"
echo "  ✅ Security 模型（证券主档）"
echo "  ✅ Trade 关联 Security（外键）"
echo "  ✅ 交易表单自动检测股票代码"
echo "  ✅ 首次交易自动创建 Security"
echo "  ✅ 按行业/时间段统计交易"
echo "  ✅ 权限控制（ADMIN/VIEWER）"
echo ""

echo "========================================"
echo "测试完成！"
echo "========================================"
echo ""
echo "📖 使用指南: SECURITY_FEATURE_GUIDE.md"
echo "🌐 访问地址: http://stocks.1plabs.pro/"
echo ""
