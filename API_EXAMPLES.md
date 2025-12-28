# Stocks-Lab API 使用示例

本文档提供常用 API 的使用示例，帮助快速集成和测试。

## 基础信息

- **Base URL**: `http://localhost:8002/api/v1`
- **认证方式**: Django Session（Cookie）
- **数据格式**: JSON
- **分页**: 默认 50 条/页

## 认证相关

### 1. 获取当前用户信息

**请求**:
```http
GET /api/v1/me/
```

**响应**:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "first_name": "",
  "last_name": ""
}
```

## 项目管理

### 1. 获取我可见的项目列表

**请求**:
```http
GET /api/v1/projects/
```

**响应**:
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "测试投资项目",
      "description": "这是一个测试项目",
      "created_by": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com"
      },
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z",
      "member_count": 2,
      "my_role": "ADMIN"
    }
  ]
}
```

### 2. 创建项目

**请求**:
```http
POST /api/v1/projects/
Content-Type: application/json

{
  "name": "价值投资项目",
  "description": "长期价值投资组合"
}
```

**响应**:
```json
{
  "id": 2,
  "name": "价值投资项目",
  "description": "长期价值投资组合",
  "created_by": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  },
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z",
  "member_count": 1,
  "my_role": "ADMIN"
}
```

**说明**: 创建者自动成为项目管理员。

### 3. 获取项目成员

**请求**:
```http
GET /api/v1/projects/1/members/
```

**响应**:
```json
[
  {
    "id": 1,
    "project": 1,
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com"
    },
    "role": "ADMIN",
    "joined_at": "2024-01-15T10:00:00Z"
  },
  {
    "id": 2,
    "project": 1,
    "user": {
      "id": 2,
      "username": "viewer",
      "email": "viewer@example.com"
    },
    "role": "VIEWER",
    "joined_at": "2024-01-15T10:05:00Z"
  }
]
```

### 4. 添加项目成员（仅管理员）

**请求**:
```http
POST /api/v1/projects/1/add_member/
Content-Type: application/json

{
  "user_id": 3,
  "role": "VIEWER"
}
```

**响应**:
```json
{
  "id": 3,
  "project": 1,
  "user": {
    "id": 3,
    "username": "newuser",
    "email": "newuser@example.com"
  },
  "role": "VIEWER",
  "joined_at": "2024-01-15T12:00:00Z"
}
```

## 日结余管理

### 1. 获取日结余列表

**请求**:
```http
GET /api/v1/balances/?project=1
```

**带日期筛选**:
```http
GET /api/v1/balances/?project=1&from_date=2024-01-01&to_date=2024-01-31
```

**响应**:
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "project": 1,
      "date": "2024-01-15",
      "balance": "165000.00",
      "notes": "今日结余",
      "created_by": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com"
      },
      "created_at": "2024-01-15T18:00:00Z",
      "updated_at": "2024-01-15T18:00:00Z",
      "attachments_count": 0
    }
  ]
}
```

### 2. 创建日结余（仅管理员）

**请求**:
```http
POST /api/v1/balances/
Content-Type: application/json

{
  "project": 1,
  "date": "2024-01-16",
  "balance": "168000.00",
  "notes": "今日盈利3000元"
}
```

**响应**:
```json
{
  "id": 11,
  "project": 1,
  "date": "2024-01-16",
  "balance": "168000.00",
  "notes": "今日盈利3000元",
  "created_by": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  },
  "created_at": "2024-01-16T18:00:00Z",
  "updated_at": "2024-01-16T18:00:00Z",
  "attachments_count": 0
}
```

### 3. 更新日结余（仅管理员）

**请求**:
```http
PATCH /api/v1/balances/11/
Content-Type: application/json

{
  "balance": "168500.00",
  "notes": "修正后的结余"
}
```

### 4. 获取净值曲线

**请求**:
```http
GET /api/v1/balance-summary/?project=1
```

**响应**:
```json
[
  {
    "date": "2024-01-15",
    "balance": "165000.00",
    "delta": "0.00",
    "return_pct": "0.0000"
  },
  {
    "date": "2024-01-16",
    "balance": "168000.00",
    "delta": "3000.00",
    "return_pct": "1.8182"
  }
]
```

**说明**: 
- `delta`: 与前一日的差额
- `return_pct`: 收益率百分比

## 交易记录管理

### 1. 获取交易列表

**基础查询**:
```http
GET /api/v1/trades/?project=1
```

**多条件筛选**:
```http
GET /api/v1/trades/?project=1&symbol=600519&side=BUY&from_date=2024-01-01&to_date=2024-01-31
```

**响应**:
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "project": 1,
      "symbol": "600519",
      "side": "BUY",
      "quantity": 100,
      "price": "1850.5000",
      "executed_at": "2024-01-10T14:30:00Z",
      "thesis": "# 茅台买入分析\n\n基于以下理由买入：\n- 业绩稳健增长\n- 估值合理\n- 长期看好",
      "thesis_html": "<h1>茅台买入分析</h1><p>基于以下理由买入：</p><ul><li>业绩稳健增长</li><li>估值合理</li><li>长期看好</li></ul>",
      "review": "",
      "review_html": "",
      "total_amount": 185050.0,
      "created_by": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com"
      },
      "created_at": "2024-01-10T15:00:00Z",
      "updated_at": "2024-01-10T15:00:00Z",
      "attachments_count": 0
    }
  ]
}
```

### 2. 创建交易记录（仅管理员）

**请求**:
```http
POST /api/v1/trades/
Content-Type: application/json

{
  "project": 1,
  "symbol": "600519",
  "side": "BUY",
  "quantity": 100,
  "price": "1850.50",
  "executed_at": "2024-01-16T10:30:00",
  "thesis": "# 买入理由\n\n技术面突破，基本面良好。",
  "review": ""
}
```

**响应**:
```json
{
  "id": 6,
  "project": 1,
  "symbol": "600519",
  "side": "BUY",
  "quantity": 100,
  "price": "1850.5000",
  "executed_at": "2024-01-16T10:30:00Z",
  "thesis": "# 买入理由\n\n技术面突破，基本面良好。",
  "thesis_html": "<h1>买入理由</h1><p>技术面突破，基本面良好。</p>",
  "review": "",
  "review_html": "",
  "total_amount": 185050.0,
  "created_by": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  },
  "created_at": "2024-01-16T10:35:00Z",
  "updated_at": "2024-01-16T10:35:00Z",
  "attachments_count": 0
}
```

**注意**: `thesis` 字段必填！

### 3. 更新交易记录（仅管理员）

**请求**:
```http
PATCH /api/v1/trades/6/
Content-Type: application/json

{
  "review": "# 复盘\n\n买入点位准确，后续继续观察。"
}
```

## 出资记录管理

### 1. 获取出资列表

**请求**:
```http
GET /api/v1/contributions/?project=1
```

**响应**:
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "project": 1,
      "user": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com"
      },
      "amount": "100000.00",
      "notes": "初始出资",
      "contributed_at": "2024-01-01",
      "created_at": "2024-01-01T10:00:00Z",
      "created_by": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com"
      }
    }
  ]
}
```

### 2. 创建出资记录（仅管理员）

**请求**:
```http
POST /api/v1/contributions/
Content-Type: application/json

{
  "project": 1,
  "user": 2,
  "amount": "50000.00",
  "contributed_at": "2024-01-15",
  "notes": "追加出资"
}
```

## 附件管理

### 1. 上传附件（仅管理员）

**请求**:
```http
POST /api/v1/attachments/
Content-Type: multipart/form-data

owner_type=TRADE
owner_id=1
file=<binary data>
```

**响应**:
```json
{
  "id": 1,
  "owner_type": "TRADE",
  "owner_id": 1,
  "file": "/media/attachments/2024/01/16/screenshot.png",
  "file_url": "http://localhost:8002/media/attachments/2024/01/16/screenshot.png",
  "file_name": "screenshot.png",
  "uploaded_by": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  },
  "uploaded_at": "2024-01-16T15:00:00Z"
}
```

### 2. 获取附件列表

**按所有者查询**:
```http
GET /api/v1/attachments/?owner_type=TRADE&owner_id=1
```

## 审计日志

### 1. 获取审计日志

**请求**:
```http
GET /api/v1/audit-logs/
```

**按模型类型筛选**:
```http
GET /api/v1/audit-logs/?model_type=Trade&model_id=1
```

**响应**:
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "action": "CREATE",
      "model_type": "Trade",
      "model_id": 1,
      "user": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com"
      },
      "changes": "{\"symbol\": \"600519\", \"side\": \"BUY\"}",
      "changes_dict": {
        "symbol": "600519",
        "side": "BUY"
      },
      "created_at": "2024-01-10T15:00:00Z"
    }
  ]
}
```

## 错误处理

### 常见 HTTP 状态码

- `200 OK`: 请求成功
- `201 Created`: 创建成功
- `400 Bad Request`: 请求参数错误
- `401 Unauthorized`: 未登录
- `403 Forbidden`: 无权限访问
- `404 Not Found`: 资源不存在
- `500 Internal Server Error`: 服务器错误

### 错误响应示例

**权限不足**:
```json
{
  "detail": "您没有执行该操作的权限。"
}
```

**参数验证失败**:
```json
{
  "thesis": ["该字段是必填项。"],
  "price": ["请确保该值大于或等于 0.0001。"]
}
```

## 使用 curl 测试

### 登录并保存 Cookie
```bash
curl -X POST http://localhost:8002/login/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" \
  -c cookies.txt
```

### 使用 Cookie 访问 API
```bash
curl -X GET http://localhost:8002/api/v1/me/ \
  -b cookies.txt
```

### 创建项目
```bash
curl -X POST http://localhost:8002/api/v1/projects/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "新项目",
    "description": "测试项目"
  }'
```

## 使用 Python Requests

```python
import requests

# 创建会话
session = requests.Session()

# 登录
login_data = {
    'username': 'admin',
    'password': 'admin123'
}
session.post('http://localhost:8002/login/', data=login_data)

# 获取当前用户
response = session.get('http://localhost:8002/api/v1/me/')
print(response.json())

# 创建项目
project_data = {
    'name': '价值投资项目',
    'description': '长期价值投资'
}
response = session.post(
    'http://localhost:8002/api/v1/projects/',
    json=project_data
)
print(response.json())

# 添加日结余
balance_data = {
    'project': 1,
    'date': '2024-01-16',
    'balance': '168000.00',
    'notes': '今日结余'
}
response = session.post(
    'http://localhost:8002/api/v1/balances/',
    json=balance_data
)
print(response.json())
```

## 注意事项

1. **CSRF Token**: Django 默认启用 CSRF 保护，使用表单提交时需要包含 CSRF token
2. **权限验证**: 所有 API 需要登录，部分操作需要管理员权限
3. **项目权限**: 必须是项目成员才能访问项目数据
4. **必填字段**: Trade 的 `thesis` 字段必填
5. **唯一约束**: DailyBalance 的 `project + date` 组合唯一

## 更多信息

- 完整文档: [README.md](README.md)
- 快速启动: [QUICKSTART.md](QUICKSTART.md)
- 部署指南: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
