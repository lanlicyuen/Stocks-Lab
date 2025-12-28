# 📊 投资项目披露平台 - 前端实现完成

## 🎉 项目概述

基于 Django + DRF 的投资项目管理与披露平台，采用 **Mobile-first 响应式设计**，支持项目管理、日结余记录、交易记录、附件上传等核心功能。

## ✨ 核心特性

### 后端架构
- ✅ Django 4.2.9 + DRF 3.14.0
- ✅ 7个数据模型（Project, ProjectMember, Contribution, DailyBalance, Trade, Attachment, AuditLog）
- ✅ 完整的 REST API（14+ endpoints）
- ✅ 资源级权限控制（ProjectPermission + AttachmentPermission）
- ✅ 安全文件访问（SecureFileDownloadView）
- ✅ Balance Summary API（净值曲线数据）

### 前端设计
- ✅ Mobile-first 响应式设计
- ✅ 底部 Tab 导航（移动端）
- ✅ 卡片式布局（移动端）+ 表格布局（桌面端）
- ✅ 基于角色的 UI 控制（ADMIN 显示新增按钮，VIEWER 隐藏编辑按钮）
- ✅ 实时 API 对接（CSRF + Session 认证）
- ✅ Markdown 渲染（交易逻辑）
- ✅ 图片附件预览

## 📁 项目结构

```
Stocks-Lab/
├── core/                      # 核心应用
│   ├── models.py             # 7个数据模型
│   ├── serializers.py        # DRF序列化器
│   ├── viewsets.py          # API ViewSets
│   ├── permissions.py        # 权限控制
│   ├── file_views.py         # 安全文件下载
│   ├── views.py             # 旧版前端视图
│   ├── views_new.py         # 新版Mobile-first视图
│   └── urls.py              # API路由
├── templates/                # 前端模板
│   ├── base_new.html        # 基础模板（Mobile-first）
│   ├── login_new.html       # 登录页
│   ├── dashboard_new.html   # Dashboard
│   ├── projects_list_new.html  # 项目列表
│   ├── balances_list_new.html  # 日结余列表
│   ├── balance_form_new.html   # 新建日结余
│   ├── trades_list_new.html    # 交易列表
│   ├── trade_form_new.html     # 新建交易
│   └── trade_detail_new.html   # 交易详情
├── media/                    # 用户上传文件
├── static/                   # 静态文件
├── stocks_lab/              # 项目配置
│   ├── settings.py
│   └── urls.py              # 主路由
├── manage.py
├── start_service.sh         # 启动脚本
└── README_FRONTEND.md       # 本文档
```

## 🚀 快速开始

### 1. 环境要求
```bash
Python 3.8+
Django 4.2.9
djangorestframework 3.14.0
```

### 2. 安装依赖
```bash
cd /home/lanlic/Html-Project/Stocks-Lab

# 创建虚拟环境（如果没有）
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install django==4.2.9 djangorestframework==3.14.0 markdown django-cors-headers
```

### 3. 数据库初始化
```bash
# 应用迁移
python manage.py migrate

# 创建测试账号
python manage.py createsuperuser --username admin --email admin@test.com
# 密码: admin123

# 创建观察者账号
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_user('viewer', 'viewer@test.com', 'viewer123')
>>> exit()
```

### 4. 启动服务
```bash
# 方式1：使用启动脚本（推荐）
./start_service.sh

# 方式2：手动启动
python manage.py runserver 0.0.0.0:20004
```

### 5. 访问应用
```
🌐 前端登录: http://localhost:20004/login/
🔧 API文档: http://localhost:20004/api/v1/
🛠️  管理后台: http://localhost:20004/admin/
```

## 👥 测试账号

| 用户名 | 密码 | 角色 | 权限 |
|--------|------|------|------|
| admin | admin123 | ADMIN | 可读写（新增、编辑、删除） |
| viewer | viewer123 | VIEWER | 只读（查看） |

## 📱 页面功能

### 登录页 (`/login/`)
- 渐变背景设计
- 测试账号展示
- 响应式布局

### Dashboard (`/`)
- 项目数统计
- 总投资金额
- 今日盈亏
- 总收益率
- 我的项目列表
- 角色徽章显示

### 项目列表 (`/projects/`)
- 移动端：卡片布局
- 桌面端：表格布局
- ADMIN 可新建项目
- 项目选择器（localStorage 持久化）

### 日结余列表 (`/balances/`)
- 日期筛选（默认最近30天）
- 移动端：卡片显示余额
- 桌面端：表格显示
- ADMIN 可新增、删除
- FAB 浮动按钮（移动端）

### 新建日结余 (`/balances/create/`)
- 日期选择（默认今天）
- 金额输入
- 备注字段
- 附件上传（多图片/PDF）
- 附件预览
- 仅 ADMIN 可访问

### 交易列表 (`/trades/`)
- 交易方向筛选（买入/卖出）
- 标的代码搜索
- 移动端：卡片显示，带方向徽章
- 桌面端：表格显示
- 成交金额高亮
- ADMIN 可新增、删除

### 新建交易 (`/trades/create/`)
- 标的代码输入
- 交易方向选择
- 价格、数量输入
- 交易日期选择
- 交易逻辑（Markdown 编辑器）
- 附件上传（多图片/PDF）
- 仅 ADMIN 可访问

### 交易详情 (`/trades/{id}/`)
- 完整交易信息展示
- Markdown 渲染的交易逻辑
- 附件图片画廊
- 点击图片放大查看
- ADMIN 可删除

## 🔐 权限体系

### 角色定义
- **ADMIN**: 项目管理员
  - 可以新增、编辑、删除所有记录
  - 可以上传附件
  - 可以邀请成员
  - 可以创建新项目

- **VIEWER**: 项目观察者
  - 只能查看项目数据
  - 不能新增、编辑、删除
  - 不能上传附件
  - UI 隐藏所有编辑按钮

### 实现机制
1. **后端**: ProjectPermission + AttachmentPermission
   - 每个 API 请求自动校验 ProjectMember
   - VIEWER 只允许 GET/HEAD/OPTIONS
   - ADMIN 允许所有操作

2. **前端**: 模板 + JavaScript
   - `user_role` 传递到模板
   - `{% if user_role == 'ADMIN' %}` 控制按钮显示
   - JavaScript API.request() 自动处理 403

## 📊 API 端点

### 项目管理
```
GET    /api/v1/projects/          - 项目列表
POST   /api/v1/projects/          - 创建项目 (ADMIN)
GET    /api/v1/projects/{id}/     - 项目详情
PUT    /api/v1/projects/{id}/     - 更新项目 (ADMIN)
DELETE /api/v1/projects/{id}/     - 删除项目 (ADMIN)
```

### 日结余
```
GET    /api/v1/balances/          - 日结余列表
POST   /api/v1/balances/          - 创建日结余 (ADMIN)
GET    /api/v1/balances/{id}/     - 日结余详情
DELETE /api/v1/balances/{id}/     - 删除日结余 (ADMIN)
GET    /api/v1/balance-summary/   - 净值曲线数据
```

### 交易记录
```
GET    /api/v1/trades/            - 交易列表
POST   /api/v1/trades/            - 创建交易 (ADMIN)
GET    /api/v1/trades/{id}/       - 交易详情
DELETE /api/v1/trades/{id}/       - 删除交易 (ADMIN)
```

### 附件管理
```
GET    /api/v1/attachments/       - 附件列表
POST   /api/v1/attachments/       - 上传附件 (ADMIN)
GET    /api/v1/attachments/{id}/download/ - 下载附件（需权限）
GET    /api/v1/attachments/{id}/info/     - 附件信息
```

## 🎨 响应式设计

### 断点
- **Mobile**: < 768px
- **Desktop**: ≥ 768px

### 移动端特性
- 底部 Tab 导航（首页、项目、数据、退出）
- 卡片式列表布局
- FAB 浮动按钮（新增操作）
- 触摸优化（active 动画）

### 桌面端特性
- 顶部导航栏
- 表格布局（可排序）
- 隐藏底部 Tab
- 隐藏 FAB（按钮在表头）

### CSS 架构
- CSS Variables（主题颜色）
- Flexbox + Grid 布局
- Media Queries（@media min-width: 768px）
- Card + Table 双重结构

## 🛠️ 开发指南

### 新增页面流程
1. 创建模板 `templates/xxx_new.html`
2. 继承 `base_new.html`
3. 在 `core/views_new.py` 添加视图函数
4. 在 `stocks_lab/urls.py` 添加路由
5. 更新底部导航链接（如需要）

### API 调用示例
```javascript
// GET 请求
const projects = await API.get('/projects/');

// POST 请求
const project = await API.post('/projects/', {
    name: 'New Project',
    description: 'Description'
});

// DELETE 请求
await API.delete('/projects/1/');

// 文件上传
const formData = new FormData();
formData.append('file', file);
formData.append('owner_type', 'TRADE');
formData.append('owner_id', tradeId);
await API.upload('/attachments/', formData);
```

### 格式化函数
```javascript
// 货币格式
formatCurrency(12345.67);  // "¥12,345.67"

// 日期格式
formatDate('2024-03-15');  // "2024-03-15"

// 日期时间格式
formatDateTime('2024-03-15T10:30:00Z');  // "2024-03-15 10:30"
```

## 🔒 安全特性

### 文件访问控制
- ❌ 禁止直接访问 `/media/` 目录
- ✅ 所有文件通过 `/api/v1/attachments/{id}/download/` 访问
- ✅ 登录校验 + 项目权限校验
- ✅ VIEWER 无法绕过权限访问文件

### CSRF 保护
- 所有 POST/PUT/DELETE 请求自动携带 CSRF Token
- API.request() 自动从 Cookie 读取并添加到 Header

### Session 认证
- Django Session Authentication
- 登录后自动维持会话
- 退出后清除会话

## 📈 后续计划

- [ ] 添加 Chart.js 图表（净值曲线）
- [ ] 实现成员管理页面
- [ ] 添加出资记录管理
- [ ] 导出功能（PDF/Excel）
- [ ] 通知功能
- [ ] 评论功能
- [ ] 移动端 PWA 支持

## 🐛 已知问题

1. ~~文件直接 URL 访问绕过权限~~ ✅ 已修复
2. ~~Balance Summary API 缺失~~ ✅ 已实现
3. ~~前端无响应式设计~~ ✅ 已完成

## 📞 技术支持

- 后端端口: 20004
- 前端访问: http://localhost:20004/
- 数据库: SQLite3 (db.sqlite3)
- 日志: django.log

## 📄 许可证

MIT License

---

**Created by GitHub Copilot** | 2024-03-15
