# 市场账户功能测试指南

## 访问路径

- **账户列表（首页）**: http://stocks.1plabs.pro/ 或 http://stocks.1plabs.pro/accounts/
- **模拟账户**: http://stocks.1plabs.pro/accounts/?mode=SIM
- **真实账户**: http://stocks.1plabs.pro/accounts/?mode=REAL

## 功能验证清单

### 1. 页面加载 ✓
- [ ] 登录后默认显示"模拟账号"模式
- [ ] "市场账户"区块正常显示
- [ ] 如果无账户，显示空态提示 + "新增市场账户"按钮

### 2. 模式切换 ✓
- [ ] 点击"模拟账号"按钮，加载 SIM 模式账户
- [ ] 点击"真实账号"按钮，加载 REAL 模式账户
- [ ] 按钮高亮状态正确切换
- [ ] 控制台输出：`Loading accounts for mode: SIM/REAL`

### 3. 创建账户 ✓
- [ ] 点击"+ 新增市场账户"弹出表单
- [ ] 选择市场类型自动推荐币种（美股→USD，A股→CNY）
- [ ] 提交成功后：
  - [ ] 显示成功提示
  - [ ] 弹窗关闭
  - [ ] 列表自动刷新，新账户出现
- [ ] 创建失败显示错误提示

### 4. 账户列表展示 ✓
每个账户卡片显示：
- [ ] 账户名称（或市场类型名称）
- [ ] 模式标签（模拟/真实）
- [ ] 市场类型
- [ ] 币种
- [ ] 起始资金
- [ ] 当前余额
- [ ] 交易笔数
- [ ] "进入账户"按钮

### 5. 进入账户详情 ✓
- [ ] 点击"进入账户"跳转到 `/accounts/{id}/`
- [ ] 详情页正常显示（如果已实现）

## API 端点测试

### 获取账户列表
```bash
# 模拟账户
curl -H "Cookie: sessionid=YOUR_SESSION" \
     http://127.0.0.1:20004/api/v1/market-accounts/?mode=SIM

# 真实账户
curl -H "Cookie: sessionid=YOUR_SESSION" \
     http://127.0.0.1:20004/api/v1/market-accounts/?mode=REAL
```

预期响应：
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
      "name": "美股",
      "currency": "USD",
      "currency_display": "美元",
      "start_cash": "100000.00",
      "current_cash": 100000.00,
      "trade_count": 0,
      "total_pnl": 0.0,
      "return_pct": 0.0,
      "created_at": "2025-12-27T..."
    }
  ]
}
```

### 创建账户
```bash
curl -X POST http://127.0.0.1:20004/api/v1/market-accounts/ \
     -H "Content-Type: application/json" \
     -H "Cookie: sessionid=YOUR_SESSION" \
     -H "X-CSRFToken: YOUR_CSRF_TOKEN" \
     -d '{
       "mode": "SIM",
       "market_type": "CN_A",
       "currency": "CNY",
       "start_cash": 50000
     }'
```

预期响应：新创建的账户对象（同上格式）

## 调试信息

打开浏览器控制台（F12），查看：

1. **网络请求**:
   - `GET /api/v1/market-accounts/?mode=SIM` - 状态 200
   - `POST /api/v1/market-accounts/` - 状态 201

2. **控制台日志**:
   ```
   Loading accounts for mode: SIM
   Loaded accounts: 2 [Array]
   Creating account: {mode: 'SIM', market_type: 'US_STOCK', ...}
   Created account: {id: 3, name: '美股', ...}
   ```

3. **错误排查**:
   - 如果返回 401: 未登录，刷新页面重新登录
   - 如果返回 403: CSRF token 问题，检查 cookies
   - 如果返回 400: 检查必填字段（market_type, currency, start_cash）

## 已知问题

- ~~mode 参数默认值~~ ✓ 已修复：后端 model 默认 'SIM'
- ~~创建后列表不刷新~~ ✓ 已修复：调用 `loadAccounts(currentMode)`
- ~~空态不显示~~ ✓ 已修复：检查 `accounts.length === 0`

## 测试数据

当前数据库已有账户：
- ID=1: 美股（SIM）, USD, $100,000
- ID=2: A股（REAL）, CNY, ¥50,000

## 下一步

- [ ] 实现账户详情页 `/accounts/{id}/`
- [ ] 添加账户编辑功能
- [ ] 添加账户删除功能（带二次确认）
- [ ] 显示持仓情况
- [ ] 显示交易历史
