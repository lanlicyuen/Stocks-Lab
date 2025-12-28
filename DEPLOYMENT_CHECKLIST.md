# Stocks-Lab 部署检查清单

## 开发环境 ✅

### 已完成项目文件
- [x] Django 项目配置（stocks_lab/）
- [x] 核心应用（core/）
- [x] 数据模型（7 个模型）
- [x] API 视图集和路由
- [x] 权限控制系统
- [x] 前端模板（9 个页面）
- [x] 管理脚本（manage.sh）
- [x] 完整文档

### 环境配置
- [x] requirements.txt
- [x] .env.example
- [x] .gitignore
- [x] manage.py

### 功能验证
- [ ] 虚拟环境创建
- [ ] 依赖安装
- [ ] 数据库迁移
- [ ] 管理员创建
- [ ] 测试数据导入
- [ ] 服务启动
- [ ] 前台访问
- [ ] 后台访问
- [ ] API 测试

## 本地测试步骤

```bash
# 1. 初始化项目
cd ~/Html-Project/Stocks-Lab
./manage.sh setup

# 2. 创建数据库
./manage.sh migrate

# 3. 创建管理员
./manage.sh admin

# 4. 创建测试数据（可选）
source venv/bin/activate
python create_test_data.py

# 5. 启动服务
./manage.sh run

# 6. 访问测试
# 前台: http://localhost:8002
# 后台: http://localhost:8002/admin
```

## 功能测试清单

### 认证测试
- [ ] 管理员登录前台
- [ ] 管理员登录后台
- [ ] 普通用户登录前台
- [ ] 退出登录

### 项目管理
- [ ] 创建项目（后台）
- [ ] 查看项目列表
- [ ] 查看项目详情
- [ ] 添加项目成员
- [ ] 验证成员角色

### 权限测试
- [ ] ADMIN 可以添加日结余
- [ ] ADMIN 可以添加交易
- [ ] VIEWER 只能查看
- [ ] 非成员无法访问（403）

### 数据管理
- [ ] 添加出资记录
- [ ] 添加日结余
- [ ] 添加交易记录
- [ ] 查看净值曲线
- [ ] 查看审计日志

### 响应式测试
- [ ] 电脑浏览器正常显示
- [ ] 手机浏览器正常显示
- [ ] 底部导航在手机显示
- [ ] 表格在手机变卡片

### API 测试
- [ ] GET /api/v1/me/
- [ ] GET /api/v1/projects/
- [ ] POST /api/v1/balances/
- [ ] POST /api/v1/trades/
- [ ] GET /api/v1/balance-summary/

## 生产部署检查清单

### 安全配置
- [ ] 修改 SECRET_KEY
- [ ] 设置 DEBUG=False
- [ ] 配置 ALLOWED_HOSTS
- [ ] 启用 HTTPS
- [ ] 配置 CSRF 设置
- [ ] 配置 CORS 白名单

### 数据库
- [ ] 切换到 PostgreSQL/MySQL
- [ ] 配置数据库连接
- [ ] 设置数据库备份
- [ ] 优化数据库索引

### 静态文件
- [ ] 收集静态文件
- [ ] 配置静态文件服务（Nginx）
- [ ] 配置 CDN（可选）

### 媒体文件
- [ ] 配置 S3 存储（推荐）
- [ ] 或配置本地存储路径
- [ ] 设置上传大小限制
- [ ] 配置图片压缩

### Web 服务器
- [ ] 安装 Gunicorn
- [ ] 配置 Gunicorn workers
- [ ] 配置 Nginx 反向代理
- [ ] 配置 SSL 证书
- [ ] 设置日志

### 监控和日志
- [ ] 配置错误日志
- [ ] 配置访问日志
- [ ] 设置日志轮转
- [ ] 配置监控告警（可选）

### 备份
- [ ] 配置自动备份脚本
- [ ] 测试备份恢复
- [ ] 设置异地备份

### 性能优化
- [ ] 启用数据库连接池
- [ ] 配置缓存（Redis）
- [ ] 启用 Gzip 压缩
- [ ] 优化静态资源

## 生产部署示例

### 1. 安装 Gunicorn
```bash
pip install gunicorn
```

### 2. 创建 Gunicorn 配置
```python
# gunicorn.conf.py
bind = "127.0.0.1:8002"
workers = 4
worker_class = "sync"
timeout = 120
accesslog = "/var/log/stocks-lab/access.log"
errorlog = "/var/log/stocks-lab/error.log"
```

### 3. 启动 Gunicorn
```bash
gunicorn -c gunicorn.conf.py stocks_lab.wsgi:application
```

### 4. Nginx 配置示例
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /static/ {
        alias /path/to/Stocks-Lab/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/Stocks-Lab/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 5. Systemd 服务配置
```ini
# /etc/systemd/system/stocks-lab.service
[Unit]
Description=Stocks-Lab Django Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/Stocks-Lab
Environment="PATH=/path/to/Stocks-Lab/venv/bin"
ExecStart=/path/to/Stocks-Lab/venv/bin/gunicorn -c gunicorn.conf.py stocks_lab.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl start stocks-lab
sudo systemctl enable stocks-lab
```

## 故障排除

### 数据库连接失败
- 检查数据库服务是否运行
- 验证连接配置
- 检查防火墙规则

### 静态文件 404
- 运行 `./manage.sh static`
- 检查 Nginx 配置
- 验证文件路径权限

### 权限错误
- 检查用户是否加入项目
- 验证角色配置
- 查看审计日志

### 性能问题
- 启用数据库查询优化
- 添加适当索引
- 考虑使用缓存
- 增加 workers 数量

## 安全建议

1. **定期更新依赖**
   ```bash
   pip list --outdated
   pip install -U <package>
   ```

2. **数据库访问控制**
   - 使用强密码
   - 限制网络访问
   - 定期备份

3. **应用层安全**
   - 启用 CSRF 保护
   - 配置 CORS 白名单
   - 使用 HTTPS
   - 设置合理的会话超时

4. **文件上传安全**
   - 验证文件类型
   - 限制文件大小
   - 扫描恶意文件

5. **日志和监控**
   - 记录所有敏感操作
   - 监控异常访问
   - 设置告警机制

## 维护计划

### 每日
- [ ] 检查服务运行状态
- [ ] 查看错误日志
- [ ] 监控系统资源

### 每周
- [ ] 数据库备份验证
- [ ] 清理临时文件
- [ ] 审查访问日志

### 每月
- [ ] 更新系统依赖
- [ ] 安全漏洞扫描
- [ ] 性能优化分析

### 每季度
- [ ] 完整备份测试
- [ ] 灾难恢复演练
- [ ] 安全审计

## 联系支持

如有问题：
1. 查看 [README.md](README.md)
2. 查看 [QUICKSTART.md](QUICKSTART.md)
3. 检查日志文件
4. 联系系统管理员
