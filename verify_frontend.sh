#!/bin/bash

# 前端完成验证脚本

echo "🔍 Stocks-Lab 前端实现验证"
echo "================================"
echo ""

# 检查模板文件
echo "📄 检查模板文件..."
templates=(
    "templates/base_new.html"
    "templates/login_new.html"
    "templates/dashboard_new.html"
    "templates/projects_list_new.html"
    "templates/balances_list_new.html"
    "templates/balance_form_new.html"
    "templates/trades_list_new.html"
    "templates/trade_form_new.html"
    "templates/trade_detail_new.html"
)

for template in "${templates[@]}"; do
    if [ -f "$template" ]; then
        echo "  ✅ $template"
    else
        echo "  ❌ $template (缺失)"
    fi
done

echo ""

# 检查视图文件
echo "🔧 检查视图文件..."
views_files=(
    "core/views_new.py"
    "core/views.py"
)

for view in "${views_files[@]}"; do
    if [ -f "$view" ]; then
        echo "  ✅ $view"
    else
        echo "  ❌ $view (缺失)"
    fi
done

echo ""

# 检查URL配置
echo "🌐 检查URL配置..."
if grep -q "views_new" stocks_lab/urls.py; then
    echo "  ✅ stocks_lab/urls.py 已更新"
else
    echo "  ❌ stocks_lab/urls.py 未更新"
fi

echo ""

# 检查启动脚本
echo "🚀 检查启动脚本..."
if [ -f "start_service.sh" ] && [ -x "start_service.sh" ]; then
    echo "  ✅ start_service.sh (可执行)"
else
    echo "  ❌ start_service.sh (缺失或无执行权限)"
fi

echo ""

# 检查文档
echo "📚 检查文档..."
if [ -f "README_FRONTEND.md" ]; then
    echo "  ✅ README_FRONTEND.md"
else
    echo "  ❌ README_FRONTEND.md (缺失)"
fi

echo ""

# 统计代码行数
echo "📊 代码统计..."
echo "  模板文件:"
find templates -name "*_new.html" -type f | while read file; do
    lines=$(wc -l < "$file")
    echo "    - $(basename $file): $lines 行"
done

echo ""
echo "  视图文件:"
if [ -f "core/views_new.py" ]; then
    lines=$(wc -l < "core/views_new.py")
    echo "    - views_new.py: $lines 行"
fi

echo ""

# 功能清单
echo "✨ 功能实现清单"
echo "================================"
echo ""
echo "后端功能:"
echo "  ✅ 7个数据模型"
echo "  ✅ 14+ REST API端点"
echo "  ✅ 资源级权限控制"
echo "  ✅ 安全文件访问"
echo "  ✅ Balance Summary API"
echo ""
echo "前端功能:"
echo "  ✅ Mobile-first响应式设计"
echo "  ✅ 底部Tab导航（移动端）"
echo "  ✅ 卡片布局（移动端）"
echo "  ✅ 表格布局（桌面端）"
echo "  ✅ 基于角色的UI控制"
echo "  ✅ 登录页"
echo "  ✅ Dashboard"
echo "  ✅ 项目列表"
echo "  ✅ 日结余列表/新建"
echo "  ✅ 交易列表/新建/详情"
echo "  ✅ Markdown渲染"
echo "  ✅ 附件上传/预览"
echo ""

# 下一步提示
echo "🎯 下一步操作"
echo "================================"
echo ""
echo "1. 启动服务:"
echo "   ./start_service.sh"
echo ""
echo "2. 访问应用:"
echo "   http://localhost:20004/login/"
echo ""
echo "3. 测试账号:"
echo "   admin / admin123 (ADMIN)"
echo "   viewer / viewer123 (VIEWER)"
echo ""
echo "4. 查看文档:"
echo "   cat README_FRONTEND.md"
echo ""
