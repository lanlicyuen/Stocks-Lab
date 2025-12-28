# 项目列表页完善 - 功能说明

## 完成的功能

### A. 右上角账号菜单 ✅

#### 1. 下拉菜单实现
- **位置**: 右上角用户徽章（显示用户名和角色）
- **触发**: 点击用户徽章弹出下拉菜单
- **菜单项**:
  - ⚙️ 账号管理 → 跳转到 `/account`
  - 🚪 登出 → 执行登出操作

#### 2. 登出功能
- **API**: `POST /api/v1/auth/logout/`
- **实现**:
  - 携带 CSRF token
  - 使用 `credentials: 'include'` 保持 session
  - 成功后清理 localStorage
  - 跳转到 `/login?next=当前页面`

#### 3. 登录状态检查
- **API**: `GET /api/v1/me/`
- **触发时机**: 每个需要认证的页面加载时
- **返回信息**:
  - 用户基本信息（用户名、邮箱）
  - `highest_role`: 用户在所有项目中的最高角色（SUPERUSER/ADMIN/VIEWER）
  - `is_superuser`: 是否为超级管理员
- **401 响应**: 自动跳转到登录页

### B. 项目编辑与删除 ✅

#### 1. 权限控制
- **后端**: 
  - `ProjectPermission` 确保 VIEWER 只能 GET
  - 只有 ADMIN 和 SUPERUSER 可以 PATCH/DELETE
  - 审计日志记录所有操作
- **前端**:
  - 编辑/删除按钮只对 ADMIN 显示
  - `my_role === 'ADMIN'` 判断

#### 2. 编辑功能
- **触发**: 点击"编辑"按钮
- **实现**: 
  - 使用 `prompt()` 获取新的项目名称和描述
  - API: `PATCH /api/v1/projects/{id}/`
  - 成功后刷新列表并提示

#### 3. 删除功能
- **二次确认**:
  1. 第一次: `confirm()` 提示删除警告
  2. 第二次: `prompt()` 要求输入项目名称确认
- **API**: `DELETE /api/v1/projects/{id}/`
- **成功后**: 刷新列表并提示

#### 4. 响应式设计
- **桌面版**: 表格展示，操作按钮在最后一列
- **移动版**: 卡片展示，操作按钮在卡片底部横向排列
- **按钮样式**:
  - 选择: 蓝色主按钮 (btn-primary)
  - 编辑: 默认按钮
  - 删除: 红色危险按钮 (btn-danger)

### C. 账号管理页面 ✅

- **路由**: `/account`
- **内容**:
  - 用户名、邮箱、最高角色
  - 加入时间、最后登录时间
  - 修改密码表单（占位，待后端实现）

## API 端点

### 后端新增 API

```python
# core/urls.py
GET  /api/v1/me/               # 获取当前用户信息（含角色）
POST /api/v1/auth/logout/      # 用户登出

# ProjectViewSet (已有，新增审计日志)
GET    /api/v1/projects/       # 列表
POST   /api/v1/projects/       # 创建（ADMIN）
PATCH  /api/v1/projects/{id}/  # 更新（ADMIN）
DELETE /api/v1/projects/{id}/  # 删除（ADMIN）
```

### 权限矩阵

| 操作 | VIEWER | ADMIN | SUPERUSER |
|------|--------|-------|-----------|
| GET 项目列表 | ✅ | ✅ | ✅ |
| GET 项目详情 | ✅ | ✅ | ✅ |
| POST 创建项目 | ❌ | ✅ | ✅ |
| PATCH 编辑项目 | ❌ | ✅ | ✅ |
| DELETE 删除项目 | ❌ | ✅ | ✅ |

## 文件修改清单

### 后端
- ✅ `core/urls.py` - 添加 logout 和完善 me API
- ✅ `core/viewsets.py` - ProjectViewSet 添加 update/destroy 审计日志

### 前端
- ✅ `templates/base_new.html` - 下拉菜单样式和 JS 功能
- ✅ `templates/projects_list_new.html` - 编辑/删除按钮和功能
- ✅ `templates/account_settings.html` - 新增账号管理页面
- ✅ `core/views_new.py` - 添加 account_settings_view
- ✅ `stocks_lab/urls.py` - 添加 /account 路由

## 测试步骤

### 1. 登录状态检查
```bash
# 未登录访问项目列表 → 应跳转登录页
curl -I http://stocks.1plabs.pro/projects/

# 登录后访问 → 应正常显示
# (需要在浏览器测试)
```

### 2. 账号菜单
- [ ] 点击右上角用户徽章弹出下拉菜单
- [ ] 点击"账号管理"跳转到 /account
- [ ] 点击"登出"执行登出并跳转登录页

### 3. 项目编辑（ADMIN）
- [ ] ADMIN 用户看到"编辑"按钮
- [ ] VIEWER 用户不显示"编辑"按钮
- [ ] 点击编辑输入新名称成功更新
- [ ] 取消编辑不做任何修改

### 4. 项目删除（ADMIN）
- [ ] ADMIN 用户看到"删除"按钮
- [ ] VIEWER 用户不显示"删除"按钮
- [ ] 点击删除显示二次确认
- [ ] 输入错误项目名称拒绝删除
- [ ] 输入正确项目名称成功删除

### 5. 移动端适配
- [ ] 手机访问项目列表显示卡片布局
- [ ] 操作按钮横向排列不换行
- [ ] 下拉菜单正常工作

## 安全考虑

1. **CSRF 保护**: 所有 POST 请求携带 CSRF token
2. **Session 认证**: 使用 Django session，不暴露 token
3. **权限验证**: 后端强制检查权限，前端只控制显示
4. **二次确认**: 删除操作要求输入项目名称确认
5. **审计日志**: 所有 CRUD 操作记录到 AuditLog

## 待实现功能

- [ ] 修改密码 API (`POST /api/v1/auth/change-password/`)
- [ ] 项目编辑使用模态框（而非 prompt）
- [ ] 批量操作（批量删除项目）
- [ ] 更详细的删除确认（显示影响的数据数量）
