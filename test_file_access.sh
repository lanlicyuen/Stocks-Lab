#!/bin/bash
# 附件上传和访问测试

echo "🔒 附件安全访问测试"
echo "================================"
echo ""

cd "$(dirname "$0")"

# 检查服务状态
echo "1️⃣  检查后端服务..."
if curl -s http://localhost:20004/api/v1/projects/ > /dev/null 2>&1; then
    echo "   ✅ 后端运行中"
else
    echo "   ❌ 后端未运行，请先启动: ./manage.sh run"
    exit 1
fi

echo ""
echo "2️⃣  运行权限测试..."
source venv/bin/activate
python test_file_permissions.py 2>&1 | grep -E "✅|❌|测试.*:|实现特性:|安全的文件访问方式:" | tail -20

echo ""
echo "================================"
echo "📝 快速参考"
echo "================================"
echo ""
echo "📤 上传附件:"
echo "   POST /api/v1/attachments/"
echo "   {owner_type: 'TRADE', owner_id: 1, file: <file>}"
echo ""
echo "🖼️  预览图片:"
echo "   GET /api/v1/attachments/{id}/download/?preview=true"
echo ""
echo "💾 下载文件:"
echo "   GET /api/v1/attachments/{id}/download/?preview=false"
echo ""
echo "ℹ️  文件信息:"
echo "   GET /api/v1/attachments/{id}/info/"
echo ""
echo "🔐 权限要求:"
echo "   ✅ 必须登录"
echo "   ✅ 必须是项目成员"
echo "   ✅ VIEWER 可以查看"
echo "   ❌ VIEWER 不能上传/删除"
echo ""
echo "⚠️  已禁用:"
echo "   ❌ 直接访问 /media/attachments/..."
echo ""
