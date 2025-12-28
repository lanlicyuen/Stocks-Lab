# 市场账户功能使用指南

## 功能概述

市场账户功能允许在单个项目内创建多个独立的交易账户，用于管理不同市场（美国股票/大陆A股/香港港股/加密货币）的资金和交易。每个账户独立计算现金余额、盈亏和收益率。

## 核心功能

### 1. 市场账户管理

#### 创建市场账户
- **路径**: 项目 Dashboard → "新增市场账户" 按钮
- **URL**: `/accounts/create/?project={project_id}`
- **权限**: 仅项目管理员（ADMIN）
- **必填字段**:
  - 账户名称：例如"美国股票账户"、"港股账户"
  - 市场类型：US_STOCK / CN_A / HK_STOCK / CRYPTO
  - 币种：USD / CNY / HKD / USDT（系统自动推荐）
  - 起始资金：账户初始投入金额

#### 查看账户详情
- **路径**: 项目 Dashboard → 点击任意账户卡片
- **URL**: `/accounts/{account_id}/`
- **显示内容**:
  - 账户基本信息（名称、市场类型、币种）
  - 资金统计（起始资金、当前现金、盈亏、收益率）
  - 交易统计（买入/卖出笔数和金额、手续费）
  - 资金调整记录
  - 最近交易记录

### 2. 交易管理

#### 新增交易
- **路径**: 项目 Dashboard → "新增交易记录" 按钮
- **URL**: `/trades/create/?project={project_id}`
- **新增字段**:
  - **市场账户**（必选）：选择交易所属的市场账户
    - 若项目只有一个账户，则自动选中并隐藏
    - 若有多个账户，需手动选择
  - **手续费**（可选）：交易手续费金额

#### 自动账户关联
- 创建交易时必须指定账户（或自动关联唯一账户）
- 后端自动计算账户现金余额：
  - 买入：扣除 `quantity * price + fee`
  - 卖出：增加 `quantity * price - fee`

### 3. 资金调整

#### 用途
用于修正账户现金余额，适用于以下场景：
- 手续费补录
- 利息收入/支出
- 滑点调整
- 其他非交易类资金变动

#### 操作步骤
1. 进入账户详情页
2. 点击"新增调整"按钮（仅管理员可见）
3. 填写：
   - 调整日期
   - 调整金额（正数=入金，负数=出金）
   - 调整原因（必填说明）
   - 附件（可选）
4. 提交后立即生效

## API 端点

### 市场账户 API

#### 列出项目下的所有账户
```http
GET /api/v1/market-accounts/?project={project_id}
```

**响应示例**:
```json
{
  "results": [
    {
      "id": 1,
      "name": "美国股票账户",
      "market_type": "US_STOCK",
      "market_type_display": "美国股票",
      "currency": "USD",
      "start_cash": 10000.00,
      "current_cash": 9500.50,
      "total_pnl": -499.50,
      "return_pct": -4.995,
      "trade_count": 5,
      "created_at": "2025-12-27T10:00:00Z"
    }
  ]
}
```

#### 获取账户详细统计
```http
GET /api/v1/market-accounts/{account_id}/summary/
```

**响应包含**:
- 基本账户信息
- `trade_stats`: 买入/卖出统计
- `adjustment_stats`: 资金调整统计

#### 创建市场账户
```http
POST /api/v1/market-accounts/
Content-Type: application/json

{
  "project": 1,
  "name": "港股账户",
  "market_type": "HK_STOCK",
  "currency": "HKD",
  "start_cash": 50000.00
}
```

### 资金调整 API

#### 列出账户的调整记录
```http
GET /api/v1/cash-adjustments/?account={account_id}
```

#### 创建资金调整
```http
POST /api/v1/cash-adjustments/
Content-Type: application/json

{
  "account": 1,
  "date": "2025-12-27",
  "amount": -50.00,
  "reason": "手续费补录"
}
```

**通过账户端点创建**:
```http
POST /api/v1/market-accounts/{account_id}/add-adjustment/
Content-Type: application/json

{
  "date": "2025-12-27",
  "amount": 100.00,
  "reason": "利息收入"
}
```

### 交易 API

#### 创建交易（关联账户）
```http
POST /api/v1/trades/
Content-Type: application/json

{
  "project": 1,
  "account": 1,
  "symbol": "AAPL",
  "side": "BUY",
  "quantity": 10,
  "price": 150.50,
  "fee": 5.00,
  "executed_at": "2025-12-27T10:00:00Z",
  "thesis": "看好苹果 Q4 财报",
  "security_name": "Apple Inc.",
  "security_asset_class": "US_STOCK"
}
```

#### 查询账户的交易
```http
GET /api/v1/trades/?account={account_id}
```

## 计算逻辑

### 当前现金余额
```
current_cash = start_cash 
             + SUM(adjustments.amount)
             - SUM(buy_trades: quantity * price + fee)
             + SUM(sell_trades: quantity * price - fee)
```

### 总盈亏
```
total_pnl = current_cash - (start_cash + SUM(adjustments.amount))
```

### 收益率
```
return_pct = (total_pnl / (start_cash + SUM(adjustments.amount))) * 100
```

## 权限说明

### 管理员（ADMIN）
- 创建/编辑/删除市场账户
- 创建交易记录
- 创建/编辑/删除资金调整
- 查看所有数据

### 观察者（VIEWER）
- 查看所有数据（只读）
- 无法创建/编辑/删除任何记录

## 使用场景示例

### 场景1：多市场投资
某投资项目同时投资美股和港股：
1. 创建"美股账户"（US_STOCK, USD, 10000）
2. 创建"港股账户"（HK_STOCK, HKD, 50000）
3. 在各自账户下记录交易
4. 分别查看每个市场的盈亏情况

### 场景2：模拟盘与实盘
同一项目下区分模拟账户和真实账户：
1. 创建"实盘账户"（CN_A, CNY, 100000）
2. 创建"模拟账户"（CN_A, CNY, 100000）
3. 记录实盘和模拟交易到不同账户
4. 对比两个账户的收益率

### 场景3：手续费修正
交易后发现手续费记录错误：
1. 进入账户详情页
2. 点击"新增调整"
3. 输入负数金额（例如 -5.00）
4. 说明"手续费补录"
5. 账户余额自动调整

## 数据库迁移

执行以下命令应用新模型：
```bash
cd /home/lanlic/Html-Project/Stocks-Lab
python manage.py migrate
```

迁移 `0004` 包含：
- 新增 `MarketAccount` 模型
- 新增 `CashAdjustment` 模型
- Trade 模型新增 `account` 和 `fee` 字段
- 已有交易的 `account` 字段允许为空（需手动关联）

## 注意事项

1. **账户不可删除**：如果账户下已有交易记录，无法删除该账户
2. **交易必须关联账户**：新交易必须选择市场账户，旧交易 account 可为空
3. **资金调整影响计算**：所有调整都会影响当前现金和盈亏计算
4. **币种一致性**：建议同一账户的所有交易使用同一币种
5. **手续费默认为0**：如不填写手续费，系统默认为0

## 前端页面

- **/projects/{id}/dashboard/** - 项目仪表盘（显示所有账户卡片）
- **/accounts/create/?project={id}** - 创建市场账户
- **/accounts/{id}/** - 账户详情（含资金调整功能）
- **/trades/create/?project={id}** - 创建交易（含账户选择）

## 版本信息

- **功能版本**: v1.0
- **创建日期**: 2025-12-27
- **数据库迁移**: 0004_trade_fee_marketaccount_cashadjustment_trade_account_and_more
