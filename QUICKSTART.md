# Stocks-Lab 快速启动指南

## 端口配置

- **前端**: http://localhost:20003
- **后端**: http://localhost:20004
- **管理**: http://localhost:20004/admin

## 一键启动（推荐）

```bash
cd ~/Html-Project/Stocks-Lab
./start_dev.sh
```

这个脚本会自动完成：
1. 检查环境依赖
2. 同时启动前后端（使用 tmux）
3. 显示访问地址

**tmux 快捷键**：
- `Ctrl+B + 0` - 切换到后端窗口
- `Ctrl+B + 1` - 切换到前端窗口
- `Ctrl+B + 2` - 切换到状态窗口
- `Ctrl+B + D` - 分离会话（后台运行）

**停止服务**：
```bash
./stop_dev.sh
```

## 手动启动步骤

### 1. 初始化项目
```bash
cd ~/Html-Project/Stocks-Lab

# 初始化后端
./manage.sh setup
./manage.sh migrate
./manage.sh admin

# 安装前端依赖
cd frontend && npm install && cd ..
```

### 2. （可选）创建测试数据
```bash
source venv/bin/activate
python create_test_data.py
```

这会自动创建：
- 管理员账户：admin / admin123
- 观察者账户：viewer / viewer123
- 一个测试项目，包含出资、日结余、交易记录

### 3. 分别启动服务

**终端 1 - 启动后端**：
```bash
cd ~/Html-Project/Stocks-Lab
./manage.sh run
```

**终端 2 - 启动前端**：
```bash
cd ~/Html-Project/Stocks-Lab/frontend
npm run dev
```

### 4. 访问系统

- **前端**: http://localhost:20003
- **后端管理**: http://localhost:20004/admin
- **API**: http://localhost:20004/api/v1

## 基本使用流程

### 1. 创建项目（管理员）
- 登录后台 → 投资项目 → 新增
- 填写项目名称和描述

### 2. 添加项目成员
- 后台 → 项目成员 → 新增
- 选择项目、用户、角色（ADMIN/VIEWER）

### 3. 添加出资记录
- 后台 → 出资记录 → 新增
- 填写出资人、金额、日期

### 4. 使用前台界面
- 登录前台
- 查看仪表盘
- 添加日结余（管理员）
- 添加交易记录（管理员）
- 查看数据（所有成员）

## 端口验证

检查服务状态：
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

## 常用命令

```bash
# 统一启动
./start_dev.sh

# 停止服务器
./stop_dev.sh

# 检查端口
./check_ports.sh

# 查看系统状态
./manage.sh status

# 备份数据库
./manage.sh backup

# 清理缓存
./manage.sh clean

# 进入 Django Shell
./manage.sh shell
```

## 端口说明

- 8002：开发服务器端口
- 可在 manage.sh 中修改端口号

## 故障排除

### 端口被占用
```bash
# 查看端口占用
lsof -i :8002

# 杀死进程
kill -9 <PID>
```

### 虚拟环境问题
```bash
# 删除重建
rm -rf venv
./manage.sh setup
```

### 数据库问题
```bash
# 备份后重建
./manage.sh backup
rm db.sqlite3
./manage.sh migrate
```

## 下一步

1. 阅读完整的 [README.md](README.md)
2. 查看 API 文档了解所有接口
3. 根据需求自定义项目
4. 部署到生产环境

## 技术支持

如有问题，请查看：
- README.md - 完整文档
- Django 官方文档
- Django REST Framework 文档
