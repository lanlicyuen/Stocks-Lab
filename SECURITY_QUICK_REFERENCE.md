# 多端安全架构 - 快速参考

## ✅ 核心保证

1. **MarketAccount.owner 外键** → 数据归属明确
2. **3 层权限防护** → 查询过滤 + 对象权限 + 创建验证
3. **JWT + Session 双认证** → Web 和 App 共用接口
4. **追加型写入** → 并发安全，无冲突

---

## 🔐 权限架构

```
认证层: JWT Token / Session
    ↓
查询过滤: get_queryset() → filter(owner=request.user)
    ↓
对象权限: IsOwner / IsAccountOwner / IsTradeOwner
    ↓
创建验证: perform_create() → get_object_or_404(owner=user)
```

---

## 🧪 安全测试结果

| 测试场景 | 结果 |
|---------|------|
| 跨用户访问账户详情 | ✅ HTTP 404 |
| 跨账户创建交易 | ✅ HTTP 404 |
| 自己账户创建交易 | ✅ HTTP 201 |
| 5 线程并发创建 | ✅ 全部成功 |

---

## 📱 多端使用示例

### Web (JWT)
```javascript
const token = localStorage.getItem('access_token');
fetch('/api/v1/accounts/', {
  headers: {'Authorization': `Bearer ${token}`}
});
```

### Flutter
```dart
final token = await storage.read(key: 'access_token');
http.get(
  Uri.parse('$baseUrl/api/v1/accounts/'),
  headers: {'Authorization': 'Bearer $token'},
);
```

---

## 📊 测试账号

- **admin** / admin123 (ID: 1) - 有 2 个账户
- **testuser** / testpass123 (ID: 2) - 有 1 个账户

---

## 🔑 关键代码

### 权限类
```python
# core/permissions.py
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.account.owner == request.user
```

### ViewSet 配置
```python
# core/viewsets.py
class TradeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAccountOwner]
    
    def get_queryset(self):
        return Trade.objects.filter(account__owner=self.request.user)
    
    def perform_create(self, serializer):
        account_id = self.request.data.get('account')
        if account_id:
            account = get_object_or_404(MarketAccount, id=account_id, owner=self.request.user)
        trade = serializer.save()
```

---

## 📖 完整文档

详细测试报告: [MULTI_CLIENT_SECURITY_REPORT.md](MULTI_CLIENT_SECURITY_REPORT.md)
