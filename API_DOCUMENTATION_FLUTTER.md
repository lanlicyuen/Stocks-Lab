# Stocks-Lab API 文档 (Flutter 移动端)

## 概述

Stocks-Lab 后端已完成 **API-first 架构改造**，完全支持 Flutter 移动端开发。

### 技术栈
- **Django 4.2.9** + Django REST Framework
- **JWT 认证**: 2小时 access token，7天 refresh token，支持自动轮换
- **双重认证**: JWT (移动端优先) + Session (Web 端兼容)
- **文件上传**: 支持 multipart/form-data，自动检测 MIME 类型
- **移动优化**: Decimal → string，DateTime → ISO8601 格式

### Base URL
- **开发环境**: `http://localhost:20004`
- **生产环境**: `https://stocks.1plabs.pro`

---

## 认证流程

### 1. 登录获取 Token

**端点**: `POST /api/v1/auth/login/`  
**权限**: 公开 (AllowAny)

**请求体**:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**响应** (200 OK):
```json
{
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@test.com",
    "first_name": "",
    "last_name": ""
  },
  "tokens": {
    "access": "eyJhbGc...",  // 2小时有效期
    "refresh": "eyJhbGc..."  // 7天有效期
  }
}
```

**错误响应** (401 Unauthorized):
```json
{
  "detail": "No active account found with the given credentials"
}
```

### 2. 刷新 Access Token

**端点**: `POST /api/v1/auth/refresh/`  
**权限**: 公开 (AllowAny)

**请求体**:
```json
{
  "refresh": "eyJhbGc..."
}
```

**响应** (200 OK):
```json
{
  "access": "eyJhbGc...",  // 新的 access token
  "refresh": "eyJhbGc..."  // 轮换后的新 refresh token
}
```

### 3. 使用 Token 访问 API

在所有需要认证的请求中，添加 HTTP Header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Flutter 示例代码**:
```dart
import 'package:http/http.dart' as http;

final response = await http.get(
  Uri.parse('https://stocks.1plabs.pro/api/v1/accounts/'),
  headers: {
    'Authorization': 'Bearer $accessToken',
    'Content-Type': 'application/json',
  },
);
```

---

## 核心 API 端点

### 账户管理 (Market Accounts)

#### 获取账户列表
```http
GET /api/v1/accounts/
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
      "owner": 1,
      "mode": "SIM",
      "mode_display": "模拟账号",
      "market_type": "US_STOCK",
      "market_type_display": "美股",
      "name": "我的美股账户",
      "currency": "USD",
      "currency_display": "美元",
      "start_cash": "10000.00",
      "created_at": "2025-12-28T01:35:02+0800",
      "updated_at": "2025-12-28T01:35:02+0800",
      "trade_count": 5,
      "current_cash": "8500.00",
      "total_pnl": "350.00",
      "return_pct": "3.50"
    }
  ]
}
```

#### 创建账户
```http
POST /api/v1/accounts/
```

**请求体**:
```json
{
  "name": "我的新账户",
  "mode": "SIM",
  "market_type": "US_STOCK",
  "currency": "USD",
  "start_cash": "10000.00"
}
```

**字段说明**:
- `mode`: `"SIM"` (模拟) 或 `"REAL"` (真实)
- `market_type`: `"US_STOCK"` (美股), `"HK_STOCK"` (港股), `"CN_STOCK"` (A股), `"CRYPTO"` (加密货币)
- `currency`: `"USD"`, `"HKD"`, `"CNY"`, `"USDT"`

#### 获取账户汇总 (Dashboard)
```http
GET /api/v1/accounts/{id}/summary/
```

**响应**:
```json
{
  "account": {
    "id": 1,
    "name": "我的美股账户",
    "mode": "SIM",
    "market_type": "US_STOCK",
    "currency": "USD"
  },
  "current_cash": "8500.00",
  "total_pnl": "350.00",
  "return_pct": "3.50",
  "summary": {
    "securities_count": 3,
    "trade_count": 5,
    "buy_trades": 3,
    "sell_trades": 2,
    "total_fees": "15.50",
    "buy_amount": "5200.00",
    "sell_amount": "3700.00"
  },
  "securities": [
    {
      "id": 1,
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "quantity": "10.00",
      "avg_price": "150.00",
      "cost_basis": "1500.00",
      "current_price": "155.00",
      "current_value": "1550.00",
      "unrealized_pnl": "50.00",
      "unrealized_pnl_pct": "3.33"
    }
  ]
}
```

**说明**: 此端点返回账户完整状态，适用于移动端首页 Dashboard。

---

### 持仓管理 (Securities)

#### 获取持仓列表
```http
GET /api/v1/securities/?account={account_id}
```

**响应**:
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "account": 1,
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "quantity": "10.00",
      "avg_price": "150.00",
      "cost_basis": "1500.00",
      "current_price": "155.00",
      "current_value": "1550.00",
      "unrealized_pnl": "50.00",
      "unrealized_pnl_pct": "3.33",
      "updated_at": "2025-12-28T10:30:00+0800"
    }
  ]
}
```

#### 更新持仓价格
```http
PATCH /api/v1/securities/{id}/
```

**请求体**:
```json
{
  "current_price": "158.50"
}
```

---

### 交易记录 (Trades)

#### 获取交易列表
```http
GET /api/v1/trades/?account={account_id}
```

**响应**:
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "account": 1,
      "symbol": "AAPL",
      "side": "BUY",
      "side_display": "买入",
      "quantity": "10.00",
      "price": "150.00",
      "fee": "5.00",
      "total_amount": "1505.00",
      "thesis": "看好苹果Q4财报",
      "executed_at": "2025-12-20T14:30:00+0800",
      "attachments": [
        {
          "id": 1,
          "file": "trade_attachments/2025/12/20/screenshot.png",
          "file_url": "https://stocks.1plabs.pro/media/trade_attachments/2025/12/20/screenshot.png",
          "file_type": "image/png",
          "file_size": 125840,
          "description": "成交截图",
          "uploaded_at": "2025-12-20T14:35:00+0800"
        }
      ],
      "attachments_count": 1
    }
  ]
}
```

#### 创建交易
```http
POST /api/v1/trades/
```

**请求体**:
```json
{
  "account": 1,
  "symbol": "AAPL",
  "side": "BUY",
  "quantity": "10.00",
  "price": "150.00",
  "fee": "5.00",
  "thesis": "看好苹果Q4财报",
  "executed_at": "2025-12-20T14:30:00+0800"
}
```

**字段说明**:
- `side`: `"BUY"` (买入) 或 `"SELL"` (卖出)
- `executed_at`: ISO8601 格式，可选时区（默认使用系统时区）

---

### 交易附件 (Trade Attachments)

#### 上传附件
```http
POST /api/v1/trade-attachments/
Content-Type: multipart/form-data
```

**请求体** (multipart/form-data):
```
trade: 1
file: (binary file)
description: "成交截图"
```

**Flutter 示例代码**:
```dart
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';

var request = http.MultipartRequest(
  'POST',
  Uri.parse('https://stocks.1plabs.pro/api/v1/trade-attachments/'),
);

request.headers['Authorization'] = 'Bearer $accessToken';
request.fields['trade'] = '1';
request.fields['description'] = '成交截图';

request.files.add(await http.MultipartFile.fromPath(
  'file',
  '/path/to/screenshot.png',
  contentType: MediaType('image', 'png'),
));

var response = await request.send();
```

**响应** (201 Created):
```json
{
  "id": 1,
  "trade": 1,
  "file": "trade_attachments/2025/12/20/screenshot.png",
  "file_url": "https://stocks.1plabs.pro/media/trade_attachments/2025/12/20/screenshot.png",
  "file_type": "image/png",
  "file_size": 125840,
  "description": "成交截图",
  "uploaded_at": "2025-12-20T14:35:00+0800"
}
```

**说明**:
- 自动检测 MIME 类型（image/png, image/jpeg, application/pdf 等）
- 自动计算文件大小
- 按日期组织文件路径: `trade_attachments/YYYY/MM/DD/`
- 只能上传属于自己账户的交易的附件

#### 获取附件列表
```http
GET /api/v1/trade-attachments/?trade={trade_id}
```

#### 删除附件
```http
DELETE /api/v1/trade-attachments/{id}/
```

---

### 资金调整 (Cash Adjustments)

#### 获取资金记录
```http
GET /api/v1/cash-adjustments/?account={account_id}
```

**响应**:
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "account": 1,
      "amount": "5000.00",
      "adjustment_type": "DEPOSIT",
      "adjustment_type_display": "入金",
      "notes": "追加本金",
      "timestamp": "2025-12-25T10:00:00+0800"
    }
  ]
}
```

#### 创建资金调整
```http
POST /api/v1/cash-adjustments/
```

**请求体**:
```json
{
  "account": 1,
  "amount": "5000.00",
  "adjustment_type": "DEPOSIT",
  "notes": "追加本金"
}
```

**字段说明**:
- `adjustment_type`: `"DEPOSIT"` (入金), `"WITHDRAWAL"` (出金), `"DIVIDEND"` (分红), `"FEE"` (费用)

---

## 用户信息

### 获取当前用户信息
```http
GET /api/v1/me/
```

**响应**:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@test.com",
  "first_name": "",
  "last_name": ""
}
```

---

## 错误处理

### 标准错误格式

**认证失败** (401 Unauthorized):
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**权限不足** (403 Forbidden):
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**资源不存在** (404 Not Found):
```json
{
  "detail": "Not found."
}
```

**字段验证失败** (400 Bad Request):
```json
{
  "symbol": ["This field is required."],
  "price": ["A valid number is required."]
}
```

---

## 数据类型说明

### Decimal 字段
所有 Decimal 字段（金额、价格、数量等）在 JSON 中返回为 **字符串格式**，避免浮点数精度问题。

**示例**:
```json
{
  "price": "150.50",     // ✅ 字符串
  "quantity": "10.00",   // ✅ 字符串
  "total": "1505.00"     // ✅ 字符串
}
```

**Flutter 解析**:
```dart
double price = double.parse(data['price']);
```

### DateTime 字段
所有日期时间字段使用 **ISO8601 格式**，包含时区信息。

**格式**: `YYYY-MM-DDTHH:MM:SS+HH:MM`

**示例**:
```json
{
  "executed_at": "2025-12-28T14:30:00+0800",  // 东八区
  "created_at": "2025-12-28T06:30:00+0000"    // UTC
}
```

**Flutter 解析**:
```dart
DateTime executedAt = DateTime.parse(data['executed_at']);
```

---

## 分页

所有列表端点支持分页参数:

**请求**:
```http
GET /api/v1/trades/?page=2&page_size=20
```

**响应**:
```json
{
  "count": 50,
  "next": "http://localhost:20004/api/v1/trades/?page=3",
  "previous": "http://localhost:20004/api/v1/trades/?page=1",
  "results": [...]
}
```

---

## 过滤与排序

### 过滤
```http
GET /api/v1/trades/?account=1&side=BUY
GET /api/v1/securities/?symbol=AAPL
```

### 排序
```http
GET /api/v1/trades/?ordering=-executed_at  # 按执行时间倒序
GET /api/v1/accounts/?ordering=name        # 按名称正序
```

---

## CORS 配置

后端已配置 CORS，允许以下来源:
- `http://localhost:3000` (React 开发环境)
- `http://localhost:20003` (Web 前端)
- 所有移动端请求 (通过 JWT 认证)

**移动端无需特殊配置**，直接使用 JWT token 即可。

---

## 安全建议

### 1. Token 存储
- **移动端**: 使用 `flutter_secure_storage` 存储 tokens
- **不要** 将 tokens 存储在 SharedPreferences 等不安全的位置

```dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

final storage = FlutterSecureStorage();

// 存储 token
await storage.write(key: 'access_token', value: accessToken);
await storage.write(key: 'refresh_token', value: refreshToken);

// 读取 token
String? accessToken = await storage.read(key: 'access_token');
```

### 2. Token 刷新策略
- Access token 有效期 2 小时
- Refresh token 有效期 7 天
- 建议在 access token 过期前 5 分钟主动刷新

```dart
// 检查 token 是否即将过期（伪代码）
if (tokenExpiresIn < 5.minutes) {
  await refreshAccessToken();
}
```

### 3. 错误处理
- **401 错误**: Token 过期或无效，尝试刷新或重新登录
- **403 错误**: 权限不足，提示用户
- **网络错误**: 显示友好提示，支持重试

---

## 测试账号

**开发环境测试账号**:
- 用户名: `admin`
- 密码: `admin123`

**生产环境**: 请注册真实账号

---

## 变更日志

### 2025-12-28 - v1.0 (API-First 架构)
- ✅ JWT 认证支持（2小时 access + 7天 refresh）
- ✅ 文件上传支持（multipart/form-data）
- ✅ 增强 summary API（新增费用和金额统计）
- ✅ Decimal → string 序列化（移动端安全）
- ✅ ISO8601 日期格式
- ✅ CORS 配置（支持跨域请求）
- ✅ 移除 Project 模块（Account-centric 架构）

---

## 联系与支持

- **开发者**: 1Plabs
- **支持邮箱**: support.1plabs.pro
- **文档仓库**: (待补充 GitHub 链接)

---

## 快速开始 Checklist

Flutter 开发者快速集成步骤:

1. ☐ 添加依赖: `http`, `flutter_secure_storage`
2. ☐ 实现 API Service 类（封装 HTTP 请求）
3. ☐ 实现登录页面（调用 `/api/v1/auth/login/`）
4. ☐ 存储 tokens 到 secure storage
5. ☐ 实现 AuthInterceptor（自动添加 Authorization header）
6. ☐ 实现 Token 刷新逻辑（401 错误时自动刷新）
7. ☐ 测试账户列表 API (`GET /api/v1/accounts/`)
8. ☐ 测试汇总 API (`GET /api/v1/accounts/{id}/summary/`)
9. ☐ 实现文件上传（交易附件）
10. ☐ 处理错误提示（401, 403, 404, 网络错误）

---

**祝开发顺利！** 🚀
