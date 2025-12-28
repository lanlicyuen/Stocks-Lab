# Stocks-Lab API 快速参考

## 🔐 认证

### 登录
```bash
POST /api/v1/auth/login/
{"username": "admin", "password": "admin123"}
→ {"tokens": {"access": "...", "refresh": "..."}}
```

### 使用 Token
```
Authorization: Bearer {access_token}
```

### 刷新 Token
```bash
POST /api/v1/auth/refresh/
{"refresh": "..."}
→ {"access": "...", "refresh": "..."}
```

---

## 📊 核心端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/accounts/` | GET | 账户列表 |
| `/api/v1/accounts/{id}/summary/` | GET | **账户汇总 (Dashboard)** |
| `/api/v1/trades/` | GET/POST | 交易记录 |
| `/api/v1/trade-attachments/` | POST | **上传附件 (multipart)** |
| `/api/v1/securities/` | GET | 持仓列表 |
| `/api/v1/cash-adjustments/` | GET/POST | 资金调整 |

---

## 📱 Flutter 示例

### 1. 登录
```dart
final response = await http.post(
  Uri.parse('$baseUrl/api/v1/auth/login/'),
  body: json.encode({'username': username, 'password': password}),
  headers: {'Content-Type': 'application/json'},
);

final data = json.decode(response.body);
final accessToken = data['tokens']['access'];
final refreshToken = data['tokens']['refresh'];

// 存储到 secure storage
await storage.write(key: 'access_token', value: accessToken);
```

### 2. 带认证的请求
```dart
final accessToken = await storage.read(key: 'access_token');

final response = await http.get(
  Uri.parse('$baseUrl/api/v1/accounts/'),
  headers: {'Authorization': 'Bearer $accessToken'},
);
```

### 3. 上传附件
```dart
var request = http.MultipartRequest(
  'POST',
  Uri.parse('$baseUrl/api/v1/trade-attachments/'),
);

request.headers['Authorization'] = 'Bearer $accessToken';
request.fields['trade'] = tradeId.toString();
request.fields['description'] = '成交截图';
request.files.add(await http.MultipartFile.fromPath('file', filePath));

final response = await request.send();
```

---

## 🎯 数据格式

### Decimal → String
```json
{
  "price": "150.50",      // ✅ 字符串
  "quantity": "10.00"     // ✅ 字符串
}
```

Flutter 解析: `double.parse(data['price'])`

### DateTime → ISO8601
```json
{
  "executed_at": "2025-12-28T14:30:00+0800"
}
```

Flutter 解析: `DateTime.parse(data['executed_at'])`

---

## ⚡ Token 生命周期

- **Access Token**: 2 小时
- **Refresh Token**: 7 天
- **策略**: 建议在过期前 5 分钟刷新 access token

---

## 🛠️ 测试命令

```bash
# 登录
curl -X POST http://localhost:20004/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 获取账户列表
curl http://localhost:20004/api/v1/accounts/ \
  -H "Authorization: Bearer {token}"

# 获取账户汇总
curl http://localhost:20004/api/v1/accounts/1/summary/ \
  -H "Authorization: Bearer {token}"
```

---

## 📝 环境信息

- **开发环境**: http://localhost:20004
- **生产环境**: https://stocks.1plabs.pro
- **测试账号**: admin / admin123
- **Django PID**: 1192307

---

## 🔗 完整文档

详细文档请查看: [API_DOCUMENTATION_FLUTTER.md](API_DOCUMENTATION_FLUTTER.md)
