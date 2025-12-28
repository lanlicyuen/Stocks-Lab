# Stocks-Lab 开发环境端口配置

## 端口分配

本项目采用前后端分离架构，固定使用以下端口：

- **前端开发服务器**: `http://localhost:20003`
- **后端 API 服务器**: `http://localhost:20004`
- **管理后台**: `http://localhost:20004/admin`

## 快速启动

### 方式一：统一启动（推荐）

使用 tmux 同时启动前后端（推荐）：

```bash
cd ~/Html-Project/Stocks-Lab
./start_dev.sh
```

这会在 tmux 会话中同时启动前端和后端，窗口切换：
- `Ctrl+B + 0` - 后端窗口
- `Ctrl+B + 1` - 前端窗口
- `Ctrl+B + 2` - 状态窗口

停止服务：
```bash
./stop_dev.sh
```

或直接关闭 tmux 会话：
```bash
tmux kill-session -t stocks-lab
```

### 方式二：分别启动

**启动后端（终端 1）：**
```bash
cd ~/Html-Project/Stocks-Lab
source venv/bin/activate
python manage.py runserver 0.0.0.0:20004
```

**启动前端（终端 2）：**
```bash
cd ~/Html-Project/Stocks-Lab/frontend
npm run dev
```

## 端口验证

检查端口状态：
```bash
./check_ports.sh
```

输出示例：
```
✅ 前端 (端口 20003): 运行中
✅ 后端 (端口 20004): 运行中
✅ 后端 API: 正常响应
✅ 前端: 正常响应
```

## 访问地址

- **前端界面**: http://localhost:20003
- **后端 API**: http://localhost:20004/api/v1
- **管理后台**: http://localhost:20004/admin
- **API 文档**: 见 API_EXAMPLES.md

## 环境变量配置

### 后端环境变量（.env）

```bash
# Django Backend Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Port Configuration
BACKEND_PORT=20004
FRONTEND_PORT=20003

# API Base URL
API_BASE_URL=http://localhost:20004/api/v1
```

### 前端环境变量（frontend/.env）

```bash
# Frontend API Configuration
VITE_API_BASE_URL=http://localhost:20004/api/v1
VITE_BACKEND_URL=http://localhost:20004
```

## CORS 配置

后端已配置允许来自前端端口的跨域请求：

**允许的来源**:
- `http://localhost:20003`
- `http://127.0.0.1:20003`

**允许凭证**: 是（支持 Cookie/Session）

**CSRF 信任来源**:
- `http://localhost:20003`
- `http://127.0.0.1:20003`

## 开发流程

### 1. 首次设置

```bash
# 初始化后端
cd ~/Html-Project/Stocks-Lab
./manage.sh setup
./manage.sh migrate
./manage.sh admin

# 安装前端依赖
cd frontend
npm install
cd ..

# 生成测试数据（可选）
source venv/bin/activate
python create_test_data.py
```

### 2. 日常开发

```bash
# 启动开发环境
./start_dev.sh

# 或分别启动
# 终端1: ./manage.sh run
# 终端2: cd frontend && npm run dev
```

### 3. 访问测试

打开浏览器访问：
- 前端: http://localhost:20003
- 后端管理: http://localhost:20004/admin

测试账户（需先运行 `create_test_data.py`）：
- 管理员: `admin` / `admin123`
- 观察者: `viewer` / `viewer123`

### 4. 停止服务

```bash
./stop_dev.sh
```

## 前端代理配置

前端开发服务器（Vite）已配置代理，自动转发以下路径到后端：

- `/api/*` → `http://localhost:20004/api/*`
- `/media/*` → `http://localhost:20004/media/*`
- `/static/*` → `http://localhost:20004/static/*`

这意味着前端可以直接使用相对路径访问 API：
```javascript
// 这两种方式等效
fetch('/api/v1/projects/')
fetch('http://localhost:20004/api/v1/projects/')
```

## API 调用示例

### 使用相对路径（推荐）

```javascript
// 前端代码（运行在 20003）
const response = await fetch('/api/v1/projects/', {
    credentials: 'include'
});
```

### 使用完整 URL

```javascript
// 使用环境变量
const API_BASE = import.meta.env.VITE_API_BASE_URL;
const response = await fetch(`${API_BASE}/projects/`, {
    credentials: 'include'
});
```

## 故障排除

### 端口被占用

```bash
# 查看端口占用
lsof -i :20003
lsof -i :20004

# 杀死进程
kill -9 <PID>

# 或使用停止脚本
./stop_dev.sh
```

### CORS 错误

确保：
1. 后端已启动在 20004
2. 前端访问地址是 `localhost:20003`（不是 `127.0.0.1:20003`）
3. 检查 `stocks_lab/settings.py` 中的 CORS 配置

### CSRF 错误

确保：
1. API 请求包含 `credentials: 'include'`
2. 检查 Cookie 中的 `csrftoken`
3. POST 请求包含 `X-CSRFToken` 头

示例：
```javascript
const csrftoken = getCookie('csrftoken');
fetch('/api/v1/projects/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json'
    },
    credentials: 'include',
    body: JSON.stringify(data)
});
```

### 前端无法连接后端

1. 检查后端是否运行：
   ```bash
   curl http://localhost:20004/api/v1/projects/
   ```

2. 检查防火墙设置

3. 确认使用 `0.0.0.0:20004` 而不是 `127.0.0.1:20004`

## 生产部署

生产环境建议：
1. 使用 Nginx 反向代理
2. 统一域名和端口（如都在 80/443）
3. 配置 SSL 证书
4. 使用环境变量配置不同的端口

详见：[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

## 管理脚本

| 脚本 | 用途 |
|------|------|
| `./start_dev.sh` | 统一启动前后端（tmux） |
| `./stop_dev.sh` | 停止所有开发服务 |
| `./check_ports.sh` | 检查端口状态 |
| `./manage.sh run` | 只启动后端 |
| `frontend/start.sh` | 只启动前端 |

## 技术架构

```
┌─────────────────────────────────────────────┐
│  前端 (Vite + 原生 JS)                      │
│  http://localhost:20003                     │
│                                             │
│  - 静态 HTML/CSS/JS                         │
│  - Vite Dev Server                          │
│  - 代理 API 请求到后端                      │
└─────────────────┬───────────────────────────┘
                  │
                  │ HTTP/AJAX
                  │ (CORS enabled)
                  │
┌─────────────────▼───────────────────────────┐
│  后端 (Django + DRF)                        │
│  http://localhost:20004                     │
│                                             │
│  - REST API (/api/v1)                       │
│  - Django Admin (/admin)                    │
│  - Session Auth + CSRF                      │
│  - SQLite Database                          │
└─────────────────────────────────────────────┘
```

## 总结

- ✅ 前端固定端口: **20003**
- ✅ 后端固定端口: **20004**
- ✅ CORS 已配置
- ✅ CSRF 已配置
- ✅ 一键启动脚本
- ✅ 端口验证工具
- ✅ 环境变量配置

所有配置已完成，可立即开发！
