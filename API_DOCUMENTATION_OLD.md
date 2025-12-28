# Stocks-Lab API 文档

## 🔐 权限模型

### 角色定义

| 角色 | 权限范围 |
|------|---------|
| **ADMIN** | 可以查看、创建、修改、删除项目内所有数据 |
| **VIEWER** | 只能查看数据，禁止任何写入操作（POST/PUT/DELETE） |
| **未加入** | 无法访问项目数据，API 返回 403 或空列表 |

### 权限检查流程

```
请求 → 认证检查 → ProjectMember 查询 → 角色验证 → 允许/拒绝
         ↓              ↓                ↓
    401 未登录    403 未加入项目    403 权限不足
```

**关键特性**:
- ✅ **资源级权限**: 所有 Project 相关资源都基于 ProjectMember 验证
- ✅ **列表级过滤**: queryset 自动过滤，只返回用户有权限的数据
- ✅ **对象级检查**: 单个对象操作时验证用户角色
- ✅ **写入保护**: VIEWER 只能执行 GET/HEAD/OPTIONS

---

## 📡 API Endpoints

**Base URL**: `http://localhost:20004/api/v1/`

### 认证

所有 API 都需要认证。使用 Django Session 认证：

```bash
# 登录
curl -X POST http://localhost:20004/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# 携带 Cookie 访问 API
curl http://localhost:20004/api/v1/projects/ \
  -H "Cookie: sessionid=xxx"
```

---

## 1️⃣ Projects（项目）

### `GET /api/v1/projects/`
获取项目列表（仅返回用户加入的项目）

**Query Parameters**:
- `name`: 按名称筛选

**Response**:
```json
[
  {
    "id": 1,
    "name": "测试投资项目",
    "description": "用于测试权限的项目",
    "created_by": {
      "id": 1,
      "username": "admin"
    },
    "created_at": "2025-12-27T09:30:00Z",
    "updated_at": "2025-12-27T09:30:00Z",
    "member_count": 2,
    "my_role": "ADMIN"
  }
]
```

---

### `POST /api/v1/projects/`
创建新项目（创建者自动成为 ADMIN）

**权限**: 任何登录用户

**Request**:
```json
{
  "name": "新项目",
  "description": "项目描述"
}
```

**Response**: `201 Created`

---

### `GET /api/v1/projects/{id}/`
获取项目详情

**权限**: ProjectMember

**Response**:
```json
{
  "id": 1,
  "name": "测试投资项目",
  "my_role": "ADMIN",
  ...
}
```

---

### `PUT /api/v1/projects/{id}/`
更新项目信息

**权限**: ADMIN only

**Request**:
```json
{
  "name": "更新后的名称",
  "description": "更新后的描述"
}
```

---

### `DELETE /api/v1/projects/{id}/`
删除项目（级联删除所有关联数据）

**权限**: ADMIN only

**Response**: `204 No Content`

---

### `GET /api/v1/projects/{id}/members/`
获取项目成员列表

**权限**: ProjectMember

**Response**:
```json
[
  {
    "id": 1,
    "user": {
      "id": 1,
      "username": "admin"
    },
    "role": "ADMIN",
    "joined_at": "2025-12-27T09:30:00Z"
  }
]
```

---

### `POST /api/v1/projects/{id}/add_member/`
添加项目成员

**权限**: ADMIN only

**Request**:
```json
{
  "user_id": 3,
  "role": "VIEWER"
}
```

---

## 2️⃣ Contributions（出资记录）

### `GET /api/v1/contributions/`
获取出资记录列表

**权限**: ProjectMember

**Query Parameters**:
- `project`: 项目 ID
- `user`: 用户 ID

**Response**:
```json
[
  {
    "id": 1,
    "project": 1,
    "user": {
      "id": 1,
      "username": "admin"
    },
    "amount": "100000.00",
    "notes": "初始投资",
    "contributed_at": "2025-12-17",
    "created_at": "2025-12-27T09:30:00Z",
    "created_by": {
      "id": 1,
      "username": "admin"
    }
  }
]
```

---

### `POST /api/v1/contributions/`
创建出资记录

**权限**: ADMIN only

**Request**:
```json
{
  "project": 1,
  "user": 1,
  "amount": "100000.00",
  "notes": "初始投资",
  "contributed_at": "2025-12-17"
}
```

**Response**: `201 Created`

---

### `GET /api/v1/contributions/{id}/`
获取出资详情

**权限**: ProjectMember

---

### `PUT /api/v1/contributions/{id}/`
更新出资记录

**权限**: ADMIN only

---

### `DELETE /api/v1/contributions/{id}/`
删除出资记录

**权限**: ADMIN only

---

## 3️⃣ Balances（每日结余）

### `GET /api/v1/balances/`
获取每日结余列表

**权限**: ProjectMember

**Query Parameters**:
- `project`: 项目 ID（必需）
- `from_date`: 起始日期（YYYY-MM-DD）
- `to_date`: 结束日期（YYYY-MM-DD）
- `date`: 精确日期

**Response**:
```json
[
  {
    "id": 1,
    "project": 1,
    "date": "2025-12-22",
    "balance": "100000.00",
    "notes": "第1天结余",
    "created_by": {
      "id": 1,
      "username": "admin"
    },
    "created_at": "2025-12-27T09:30:00Z",
    "updated_at": "2025-12-27T09:30:00Z",
    "attachments_count": 2
  }
]
```

---

### `POST /api/v1/balances/`
创建每日结余

**权限**: ADMIN only

**约束**: `(project, date)` 唯一，同一天只能有一条记录

**Request**:
```json
{
  "project": 1,
  "date": "2025-12-27",
  "balance": "105000.00",
  "notes": "交易后结余"
}
```

**Response**: `201 Created`

---

### `PUT /api/v1/balances/{id}/`
更新结余记录（会记录审计日志）

**权限**: ADMIN only

---

## 4️⃣ Balance Summary（净值曲线）⭐

### `GET /api/v1/balance-summary/`
获取项目净值曲线汇总

**权限**: ProjectMember

**Query Parameters**:
- `project`: 项目 ID（必需）

**Response**:
```json
[
  {
    "date": "2025-12-22",
    "balance": "100000.00",
    "delta": "0.00",
    "return_pct": "0.0000"
  },
  {
    "date": "2025-12-23",
    "balance": "101000.00",
    "delta": "1000.00",
    "return_pct": "1.0000"
  },
  {
    "date": "2025-12-24",
    "balance": "102000.00",
    "delta": "1000.00",
    "return_pct": "0.9901"
  }
]
```

**字段说明**:
- `date`: 日期
- `balance`: 当日账户余额
- `delta`: 相比前一天的变动金额
- `return_pct`: 日收益率（%）

**用途**: 前端绘制净值曲线图，展示资金变化趋势

---

## 5️⃣ Trades（交易记录）

### `GET /api/v1/trades/`
获取交易记录列表

**权限**: ProjectMember

**Query Parameters**:
- `project`: 项目 ID
- `symbol`: 股票代码
- `side`: 交易方向（BUY/SELL）
- `from_date`: 起始日期（YYYY-MM-DD）
- `to_date`: 结束日期（YYYY-MM-DD）

**Response**:
```json
[
  {
    "id": 1,
    "project": 1,
    "symbol": "AAPL",
    "side": "BUY",
    "quantity": 100,
    "price": "150.2500",
    "executed_at": "2025-12-24T17:23:05Z",
    "thesis": "# 买入理由\n\n技术突破，RSI 超买信号确认。",
    "thesis_html": "<h1>买入理由</h1><p>技术突破，RSI 超买信号确认。</p>",
    "review": "",
    "review_html": "",
    "total_amount": 15025.00,
    "created_by": {
      "id": 1,
      "username": "admin"
    },
    "created_at": "2025-12-27T09:30:00Z",
    "updated_at": "2025-12-27T09:30:00Z",
    "attachments_count": 1
  }
]
```

---

### `POST /api/v1/trades/`
创建交易记录

**权限**: ADMIN only

**Request**:
```json
{
  "project": 1,
  "symbol": "TSLA",
  "side": "SELL",
  "quantity": 50,
  "price": "250.75",
  "executed_at": "2025-12-27T10:00:00Z",
  "thesis": "# 卖出理由\n\n达到目标价位，技术指标超买。",
  "review": ""
}
```

**必填字段**:
- `thesis`: 交易理论依据（支持 Markdown 格式）

**Response**: `201 Created`

---

### `PUT /api/v1/trades/{id}/`
更新交易记录（可补充复盘内容）

**权限**: ADMIN only

**Request**:
```json
{
  "review": "# 复盘\n\n交易执行顺利，价格符合预期。"
}
```

---

## 6️⃣ Attachments（附件）

### `GET /api/v1/attachments/`
获取附件列表

**权限**: ProjectMember（通过 owner 对象验证项目权限）

**Query Parameters**:
- `owner_type`: 所属类型（TRADE/BALANCE）
- `owner_id`: 所属对象 ID

**Response**:
```json
[
  {
    "id": 1,
    "owner_type": "TRADE",
    "owner_id": 1,
    "file": "/media/attachments/2025/12/27/screenshot.png",
    "file_url": "http://localhost:20004/media/attachments/2025/12/27/screenshot.png",
    "file_name": "screenshot.png",
    "uploaded_by": {
      "id": 1,
      "username": "admin"
    },
    "uploaded_at": "2025-12-27T10:00:00Z"
  }
]
```

---

### `POST /api/v1/attachments/`
上传附件

**权限**: ADMIN only

**Request**: `multipart/form-data`
```
owner_type: TRADE
owner_id: 1
file: <binary data>
```

**Response**: `201 Created`

---

### `DELETE /api/v1/attachments/{id}/`
删除附件

**权限**: ADMIN only

---

## 7️⃣ Audit Logs（审计日志）

### `GET /api/v1/audit-logs/`
获取审计日志（只读）

**权限**: 
- 超级管理员：查看所有日志
- 普通用户：只能查看自己的操作日志

**Query Parameters**:
- `action`: 操作类型（CREATE/UPDATE/DELETE）
- `model_type`: 模型类型
- `model_id`: 模型 ID

**Response**:
```json
[
  {
    "id": 1,
    "action": "CREATE",
    "model_type": "Trade",
    "model_id": 1,
    "user": {
      "id": 1,
      "username": "admin"
    },
    "changes": "{\"symbol\":\"AAPL\",\"side\":\"BUY\"}",
    "changes_dict": {
      "symbol": "AAPL",
      "side": "BUY"
    },
    "created_at": "2025-12-27T09:30:00Z"
  }
]
```

---

## 🚦 HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 OK | 请求成功 |
| 201 Created | 创建成功 |
| 204 No Content | 删除成功 |
| 400 Bad Request | 请求参数错误 |
| 401 Unauthorized | 未登录 |
| 403 Forbidden | 权限不足或未加入项目 |
| 404 Not Found | 资源不存在 |
| 500 Internal Server Error | 服务器错误 |

---

## 🔒 权限场景示例

### 场景 1: ADMIN 用户
```bash
# ✅ 查看项目列表
GET /api/v1/projects/

# ✅ 创建出资记录
POST /api/v1/contributions/
{
  "project": 1,
  "user": 1,
  "amount": "50000.00",
  "contributed_at": "2025-12-27"
}

# ✅ 更新结余
PUT /api/v1/balances/1/
{
  "balance": "106000.00"
}

# ✅ 删除交易
DELETE /api/v1/trades/1/
```

---

### 场景 2: VIEWER 用户
```bash
# ✅ 查看项目列表
GET /api/v1/projects/

# ✅ 查看结余曲线
GET /api/v1/balance-summary/?project=1

# ❌ 禁止创建出资（返回 403）
POST /api/v1/contributions/
{
  "project": 1,
  "amount": "10000.00"
}
=> 403 Forbidden

# ❌ 禁止修改交易（返回 403）
PUT /api/v1/trades/1/
=> 403 Forbidden
```

---

### 场景 3: 未加入项目的用户
```bash
# ✅ 查看项目列表（返回空数组）
GET /api/v1/projects/
=> []

# ❌ 访问具体项目（返回 404）
GET /api/v1/projects/1/
=> 404 Not Found

# ❌ 访问结余列表（返回空数组）
GET /api/v1/balances/?project=1
=> []

# ❌ 创建出资（返回 403）
POST /api/v1/contributions/
{
  "project": 1,
  "amount": "10000.00"
}
=> 403 Forbidden
```

---

## 📊 测试账户

运行 `python test_api_permissions.py` 后可用：

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | ADMIN（完全权限） |
| viewer | viewer123 | VIEWER（只读） |
| outsider | outsider123 | 未加入项目 |

---

## 🧪 测试命令

```bash
# 1. 运行权限测试
python test_api_permissions.py

# 2. 启动后端服务
./manage.sh run

# 3. 使用 curl 测试 API
# 登录
curl -X POST http://localhost:20004/api/auth/login/ \
  -c cookies.txt \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 获取项目列表
curl http://localhost:20004/api/v1/projects/ \
  -b cookies.txt

# 获取净值曲线
curl "http://localhost:20004/api/v1/balance-summary/?project=1" \
  -b cookies.txt
```

---

## 📝 开发注意事项

### 1. 权限检查顺序
```python
1. IsAuthenticated: 验证登录状态
2. ProjectPermission: 验证 ProjectMember 关系
3. has_object_permission: 验证角色权限
```

### 2. queryset 自动过滤
```python
# ViewSet 的 get_queryset 自动过滤
def get_queryset(self):
    if not self.request.user.is_superuser:
        return Model.objects.filter(
            project__members__user=self.request.user
        ).distinct()
```

### 3. 审计日志自动记录
```python
# 创建/更新/删除操作自动创建 AuditLog
create_audit_log('CREATE', 'Trade', trade.id, request.user, {...})
```

### 4. Attachment 权限验证
```python
# 通过 owner 对象间接验证项目权限
attachment.get_owner().project → ProjectMember 验证
```

---

**版本**: v1.0  
**更新时间**: 2025-12-27  
**Base URL**: http://localhost:20004/api/v1/
