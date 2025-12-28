# Stocks-Lab 项目重构验证清单

## ✅ 改造完成清单

### 后端验证
- [x] 模型层：删除 Project/ProjectMember/Contribution/DailyBalance/Attachment
- [x] 模型层：保留 MarketAccount/Security/Trade/CashAdjustment/AuditLog
- [x] Serializers：删除项目相关序列化器
- [x] ViewSets：改为 owner-based 权限，删除项目相关ViewSet
- [x] URLs：路由从 /market-accounts 改为 /accounts
- [x] Admin：只注册账户相关模型
- [x] 数据库迁移：完全重建成功
- [x] 超级用户创建：admin/admin123

### 前端验证
- [x] views_new.py：简化为 4 个视图函数
- [x] stocks_lab/urls.py：删除项目相关路由
- [x] base_new.html：更新底部导航，修复 API.delete()
- [x] accounts_list.html：API 路径改为 /accounts
- [x] account_detail.html：API 路径改为 /accounts
- [x] 删除 projects_list_new.html 模板

### 服务验证
- [x] Django 服务启动成功（PID: 1175033）
- [x] API 端点响应正常（需要认证）
- [x] 未登录自动重定向到登录页（302）

---

## 🧪 功能测试计划

### 1. 登录测试
```
1. 访问 http://localhost:20004/
2. 应该自动重定向到 /login/
3. 输入 admin / admin123
4. 登录成功后跳转到 /accounts/（账户列表）
```

### 2. 账户管理测试
```
创建账户：
1. 点击"新增市场账户"按钮
2. 选择市场类型（如：美股）
3. 输入账户名称和起始资金
4. 选择模式（模拟/真实）
5. 提交，应该创建成功并刷新列表

查看账户：
1. 点击账户卡片的"进入账户"按钮
2. 应该跳转到账户详情页 /accounts/{id}/
3. 显示账户基本信息、统计数据

模式切换：
1. 在账户列表页点击"模拟账号"/"真实账号"切换器
2. 列表应该只显示对应模式的账户
```

### 3. API 测试（使用 curl）
```bash
# 获取 CSRF token（需要先登录）
curl -c cookies.txt http://localhost:20004/login/

# 登录
curl -b cookies.txt -c cookies.txt -X POST \
  -d "username=admin&password=admin123&csrfmiddlewaretoken=TOKEN" \
  http://localhost:20004/login/

# 获取账户列表
curl -b cookies.txt http://localhost:20004/api/v1/accounts/

# 创建账户
curl -b cookies.txt -X POST \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: TOKEN" \
  -d '{"mode":"SIM","market_type":"US_STOCK","start_cash":"10000"}' \
  http://localhost:20004/api/v1/accounts/
```

### 4. 删除操作测试
```
1. 创建一个测试账户
2. 在 Django Admin 中删除该账户
3. 确认无关联数据阻止删除
4. 检查审计日志是否记录删除操作
```

---

## 🔍 问题排查指南

### 检查日志
```bash
cd /home/lanlic/Html-Project/Stocks-Lab
tail -f django.log
```

### 检查数据库
```bash
sqlite3 db.sqlite3
.tables
.schema core_marketaccount
SELECT * FROM core_marketaccount;
.quit
```

### 检查迁移状态
```bash
python manage.py showmigrations
```

### 重启服务
```bash
lsof -ti:20004 | xargs kill -9
python manage.py runserver 0.0.0.0:20004
```

---

## 📝 API 端点清单

### 账户管理
- `GET    /api/v1/accounts/` - 账户列表
- `POST   /api/v1/accounts/` - 创建账户
- `GET    /api/v1/accounts/{id}/` - 账户详情
- `PUT    /api/v1/accounts/{id}/` - 更新账户
- `PATCH  /api/v1/accounts/{id}/` - 部分更新
- `DELETE /api/v1/accounts/{id}/` - 删除账户
- `GET    /api/v1/accounts/{id}/summary/` - 账户汇总
- `GET    /api/v1/accounts/{id}/trades/` - 账户交易
- `GET    /api/v1/accounts/{id}/adjustments/` - 资金调整

### 标的管理
- `GET    /api/v1/securities/` - 标的列表
- `POST   /api/v1/securities/` - 创建标的
- `GET    /api/v1/securities/{id}/` - 标的详情

### 交易管理
- `GET    /api/v1/trades/` - 交易列表
- `POST   /api/v1/trades/` - 创建交易
- `GET    /api/v1/trades/{id}/` - 交易详情
- `PUT    /api/v1/trades/{id}/` - 更新交易
- `DELETE /api/v1/trades/{id}/` - 删除交易

### 资金调整
- `GET    /api/v1/cash-adjustments/` - 调整列表
- `POST   /api/v1/cash-adjustments/` - 创建调整

### 其他
- `GET    /api/v1/me/` - 当前用户信息
- `POST   /api/v1/auth/logout/` - 登出
- `GET    /api/v1/audit-logs/` - 审计日志

---

## 📊 数据模型关系

```
User (Django 内置)
  └── MarketAccount (owner)
        ├── Security (account)
        │     └── Trade (security)
        ├── Trade (account)
        └── CashAdjustment (account)

AuditLog (user) - 独立记录所有操作
```

---

## 🎯 已实现的核心功能

### 账户系统
- ✅ 创建多个账户
- ✅ 模拟/真实模式切换
- ✅ 多市场支持（美股/港股/A股/加密货币）
- ✅ 自动币种匹配
- ✅ 起始资金设置

### 数据隔离
- ✅ 按 owner 过滤（用户只能看到自己的数据）
- ✅ 按 mode 过滤（模拟/真实数据分离）
- ✅ 每账户独立的标的库

### 统计计算
- ✅ 当前现金余额（考虑交易和调整）
- ✅ 总盈亏
- ✅ 收益率百分比
- ✅ 交易笔数统计

### 安全性
- ✅ 登录认证（Session-based）
- ✅ CSRF 保护
- ✅ Owner-based 权限控制
- ✅ 审计日志记录

---

## 🚀 性能优化建议

### 数据库索引（已实现）
```python
# MarketAccount
indexes = [
    Index(fields=['owner', 'mode']),
    Index(fields=['owner', 'market_type']),
]

# Security
indexes = [
    Index(fields=['account', 'asset_class']),
    Index(fields=['account', 'sector']),
]
unique_together = ['account', 'symbol']

# CashAdjustment
indexes = [
    Index(fields=['account', 'date']),
]
```

### 未来优化点
- [ ] 账户汇总数据缓存（Redis）
- [ ] 交易列表分页优化
- [ ] 标的信息缓存（避免重复查询）
- [ ] 使用 select_related/prefetch_related 优化查询

---

## 📚 技术栈

- **Backend**: Django 4.2.9 + Django REST Framework
- **Database**: SQLite3（开发环境）
- **Frontend**: 纯 JavaScript（无框架）
- **Auth**: Session-based authentication
- **API**: RESTful with DRF ViewSets
- **CSS**: 自定义响应式样式

---

## 📞 支持信息

**项目路径**: `/home/lanlic/Html-Project/Stocks-Lab`  
**服务端口**: `20004`  
**日志文件**: `django.log`  
**数据库**: `db.sqlite3`  
**文档**: `PROJECT_REFACTORING_SUMMARY.md`  

**管理员账号**:
- 用户名: `admin`
- 密码: `admin123`

**访问地址**:
- 本地: http://localhost:20004/
- 远程: http://stocks.1plabs.pro（需配置）

---

**最后更新**: 2025-12-28  
**状态**: ✅ 已完成并可运行
