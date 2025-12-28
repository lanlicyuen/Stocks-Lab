# Stocks-Lab - 投资项目只读披露平台

这是一个基于 Django + Django REST Framework 的投资项目披露平台，支持项目管理、出资记录、日结余记录、交易记录等功能。采用 Mobile-first 响应式设计，支持电脑和手机浏览。

## 功能特性

### 核心功能
- **项目管理**：创建和管理多个投资项目
- **成员权限**：基于项目的角色权限控制（ADMIN/VIEWER）
- **出资记录**：记录项目成员的出资信息
- **日结余**：每日手动记录账户余额，支持净值曲线查看
- **交易记录**：详细记录每笔交易，包含理论依据和复盘
- **附件管理**：支持交易和日结余添加图片附件
- **审计日志**：自动记录所有关键操作

### 权限控制
- 资源级权限基于 ProjectMember
- 未加入项目的用户无法访问项目数据（403）
- VIEWER 角色只能查看（GET/HEAD/OPTIONS）
- ADMIN 角色可以进行所有操作（POST/PUT/PATCH/DELETE）
- 附件访问也需要验证项目权限

### 前端特性
- Mobile-first 响应式设计
- 手机底部 Tab 导航
- 大按钮友好操作
- 数字键盘输入
- 卡片式列表展示
- Markdown 支持（交易依据和复盘）

## 快速开始

### 1. 环境要求
- Python 3.8+
- Node.js 16+ 和 npm
- pip

### 2. 初始化项目

```bash
# 进入项目目录
cd ~/Html-Project/Stocks-Lab

# 初始化后端
./manage.sh setup
./manage.sh migrate
./manage.sh admin

# 安装前端依赖
cd frontend && npm install && cd ..

# （可选）生成测试数据
source venv/bin/activate
python create_test_data.py
```

### 3. 启动开发环境

**方式一：统一启动（推荐）**
```bash
./start_dev.sh
```

这会使用 tmux 同时启动前后端服务。

**方式二：分别启动**
```bash
# 终端 1 - 启动后端（端口 20004）
./manage.sh run

# 终端 2 - 启动前端（端口 20003）
cd frontend && npm run dev
```

### 4. 访问系统

- **前端界面**: http://localhost:20003
- **后端管理**: http://localhost:20004/admin
- **API 端点**: http://localhost:20004/api/v1

测试账户（运行 `create_test_data.py` 后）：
- 管理员: `admin` / `admin123`
- 观察者: `viewer` / `viewer123`

### 5. 停止服务

```bash
./stop_dev.sh
```

**详细端口配置说明**: 见 [PORT_CONFIGURATION.md](PORT_CONFIGURATION.md)

## 使用流程

### 创建项目和添加成员

1. 使用管理员账户登录后台：http://localhost:8002/admin
2. 在 "投资项目" 中创建新项目
3. 在 "项目成员" 中添加成员：
   - 选择项目
   - 选择用户
   - 设置角色（ADMIN 或 VIEWER）

### 添加出资记录

1. 进入后台 "出资记录"
2. 点击 "新增出资记录"
3. 填写出资信息：
   - 选择项目
   - 选择出资人
   - 填写金额
   - 填写出资日期

### 使用前端界面

1. 使用普通用户登录前台：http://localhost:8002
2. 在仪表盘选择项目
3. 管理员可以：
   - 添加日结余记录
   - 添加交易记录
   - 查看所有数据
4. 观察者可以：
   - 查看日结余
   - 查看交易记录
   - 查看出资记录

## 端口配置

本项目采用前后端分离架构：

- **前端开发服务器**: http://localhost:20003
- **后端 API 服务器**: http://localhost:20004

详细配置见：[PORT_CONFIGURATION.md](PORT_CONFIGURATION.md)

## API 端点

**Base URL**: `http://localhost:20004/api/v1`

### 认证
- `POST /login/` - 登录（Django session）
- `POST /logout/` - 登出
- `GET /api/v1/me/` - 获取当前用户信息

### 项目
- `GET /api/v1/projects/` - 获取我可见的项目列表
- `POST /api/v1/projects/` - 创建项目（自动成为管理员）
- `GET /api/v1/projects/{id}/` - 获取项目详情
- `GET /api/v1/projects/{id}/members/` - 获取项目成员
- `POST /api/v1/projects/{id}/add_member/` - 添加成员（仅管理员）

### 出资记录
- `GET /api/v1/contributions/` - 获取出资记录列表
- `POST /api/v1/contributions/` - 创建出资记录（仅管理员）
- `GET /api/v1/contributions/{id}/` - 获取出资记录详情

### 日结余
- `GET /api/v1/balances/` - 获取日结余列表
  - 查询参数：`project`, `from_date`, `to_date`
- `POST /api/v1/balances/` - 创建日结余（仅管理员）
- `GET /api/v1/balances/{id}/` - 获取日结余详情
- `PATCH /api/v1/balances/{id}/` - 更新日结余（仅管理员）

### 净值曲线
- `GET /api/v1/balance-summary/?project={id}` - 获取项目净值曲线
  - 返回：`[{date, balance, delta, return_pct}]`

### 交易记录
- `GET /api/v1/trades/` - 获取交易记录列表
  - 查询参数：`project`, `symbol`, `side`, `from_date`, `to_date`
- `POST /api/v1/trades/` - 创建交易记录（仅管理员）
- `GET /api/v1/trades/{id}/` - 获取交易记录详情
- `PATCH /api/v1/trades/{id}/` - 更新交易记录（仅管理员）

### 附件
- `GET /api/v1/attachments/` - 获取附件列表
  - 查询参数：`owner_type`, `owner_id`
- `POST /api/v1/attachments/` - 上传附件（仅管理员）
- `GET /api/v1/attachments/{id}/` - 获取附件详情

### 审计日志
- `GET /api/v1/audit-logs/` - 获取审计日志（只能看到自己的操作）
  - 查询参数：`action`, `model_type`, `model_id`

## 管理命令

```bash
# 统一启动前后端
./start_dev.sh

# 停止所有服务
./stop_dev.sh

# 检查端口状态
./check_ports.sh

# 查看系统状态
./manage.sh status

# 执行数据库迁移
./manage.sh migrate

# 创建管理员
./manage.sh admin

# 启动后端服务器（端口 20004）
./manage.sh run

# 启动前端服务器（端口 20003）
cd frontend && npm run dev

# 进入 Django Shell
./manage.sh shell

# 收集静态文件
./manage.sh static

# 清理缓存文件
./manage.sh clean

# 备份数据库
./manage.sh backup
```

## 项目结构

```
Stocks-Lab/
├── manage.py                 # Django 管理脚本
├── manage.sh                 # 项目管理脚本
├── requirements.txt          # Python 依赖
├── .env.example             # 环境变量示例
├── .gitignore               # Git 忽略文件
├── db.sqlite3               # SQLite 数据库
├── stocks_lab/              # Django 项目配置
│   ├── __init__.py
│   ├── settings.py          # 项目设置
│   ├── urls.py              # 主路由配置
│   ├── wsgi.py
│   └── asgi.py
├── core/                     # 核心应用
│   ├── __init__.py
│   ├── models.py            # 数据模型
│   ├── serializers.py       # DRF 序列化器
│   ├── viewsets.py          # DRF 视图集
│   ├── views.py             # 前端视图
│   ├── permissions.py       # 权限类
│   ├── urls.py              # API 路由
│   ├── admin.py             # 管理后台配置
│   └── apps.py
├── templates/                # 前端模板
│   ├── base.html            # 基础模板
│   ├── login.html           # 登录页
│   ├── dashboard.html       # 仪表盘
│   ├── projects.html        # 项目列表
│   ├── project_detail.html  # 项目详情
│   ├── balances.html        # 日结余
│   ├── trades.html          # 交易记录
│   ├── contributions.html   # 出资记录
│   └── 403.html            # 无权限页面
├── media/                    # 媒体文件（附件存储）
└── static/                   # 静态文件
```

## 技术栈

### 后端
- Django 4.2.9
- Django REST Framework 3.14.0
- django-cors-headers 4.3.1
- django-filter 23.5
- Pillow 10.1.0（图片处理）
- Markdown 3.5.1（Markdown 渲染）

### 前端
- Django Templates
- 原生 JavaScript（Fetch API）
- 响应式 CSS（Mobile-first）

### 数据库
- SQLite3（开发环境）
- 可轻松切换到 PostgreSQL/MySQL

## 开发说明

### 添加新功能

1. 修改 `core/models.py` 添加新模型
2. 运行 `./manage.sh migrate` 创建数据库表
3. 在 `core/serializers.py` 添加序列化器
4. 在 `core/viewsets.py` 添加视图集
5. 在 `core/urls.py` 注册路由
6. 在 `core/admin.py` 注册管理后台

### 自定义权限

在 `core/permissions.py` 中继承 `BasePermission` 类，实现自定义权限逻辑。

### 添加审计日志

使用 `create_audit_log()` 函数记录操作：

```python
from core.viewsets import create_audit_log

create_audit_log(
    action='CREATE',  # CREATE/UPDATE/DELETE
    model_type='YourModel',
    model_id=obj.id,
    user=request.user,
    changes={'field': 'value'}
)
```

## 生产部署建议

1. **更改 SECRET_KEY**：生成新的密钥并设置到 `.env`
2. **关闭 DEBUG**：设置 `DEBUG=False`
3. **配置 ALLOWED_HOSTS**：添加您的域名
4. **使用 PostgreSQL**：替换 SQLite 数据库
5. **配置 S3**：将附件存储迁移到 S3
6. **使用 Nginx + Gunicorn**：生产环境 Web 服务器
7. **启用 HTTPS**：配置 SSL 证书
8. **收集静态文件**：运行 `./manage.sh static`

## 常见问题

### Q: 如何重置密码？
A: 使用管理后台或 Django Shell：
```python
from django.contrib.auth.models import User
user = User.objects.get(username='用户名')
user.set_password('新密码')
user.save()
```

### Q: 如何备份数据？
A: 运行 `./manage.sh backup` 自动备份 SQLite 数据库。

### Q: 如何切换到 PostgreSQL？
A: 修改 `stocks_lab/settings.py` 中的 `DATABASES` 配置。

### Q: 附件上传失败？
A: 检查 `media/` 目录权限，确保 Django 进程有写入权限。

## 许可证

本项目仅供学习和个人使用。

## 联系方式

如有问题或建议，请联系项目维护者。

---

**注意**：这是一个披露平台，不是交易系统，不接入券商 API。所有数据均为手动录入。
