# 标的主档 (Security Master) 功能使用指南

## 功能概述

"标的主档 Security Master"功能用于管理交易标的的完整信息，包括股票代码、公司名称、资产类别（美股/港股/加密货币）、行业分类等，并支持多维度的交易复盘统计。

## 核心特性

### 1. 标的主档管理
- **自动化创建**：首次交易某个标的时，系统会提示补充资产信息
- **信息记录**：记录标的代码、公司/资产全名、资产类别、行业分类、交易所
- **唯一性保证**：每个项目内标的代码唯一，避免重复录入
- **资产分类**：支持美股、港股、加密货币三种资产类别

### 2. 智能交易表单
- **实时检测**：输入标的代码时自动查询是否已存在
- **自动补全**：已存在的标的自动显示完整信息（资产类别、公司名称、行业等）
- **一次录入**：新标的只需在第一次交易时补充信息

### 3. 多维度复盘统计
- **资产类别筛选**：按美股/港股/加密货币分类查看
- **行业分类统计**：按行业分组统计交易数据
- **时间筛选**：支持自定义时间范围查询
- **数据汇总**：自动计算买入/卖出总额、净流量等指标

## 使用流程

### 步骤 1：创建交易记录（首次）

1. 进入项目 Dashboard，点击"新增交易记录"
2. 输入标的代码（如：AAPL），系统自动检测
3. 如果是首次交易该标的：
   - 系统展开"补充信息"区块
   - 填写：
     - **资产类别**（必填）：美股 / 港股 / 加密货币
     - **公司/资产全名**（必填）：例如 Apple Inc. 或 Bitcoin
     - **行业分类**（可选）：例如 科技
     - **交易所**（可选）：NASDAQ / NYSE / HKEX / Binance 等
4. 填写交易详情（价格、数量、日期、理由）
5. 提交后，系统自动创建 Security 记录并关联

### 步骤 2：后续交易（自动关联）

1. 再次交易同一标的
2. 输入代码后，系统自动显示：
   - 资产类别
   - 公司/资产名称
   - 行业分类（如有）
   - 交易所（如有）
3. 无需再次填写标的信息，直接填写交易详情即可

### 步骤 3：查看分类复盘

1. 在项目 Dashboard 点击"分类复盘统计"
2. 设置筛选条件：
   - **时间范围**：选择开始和结束日期（默认最近30天）
   - **资产类别**：选择美股/港股/加密货币或查看全部
   - **行业筛选**：选择特定行业或查看全部
3. 点击"查询"查看统计结果

## 统计报表说明

### 统计概览
- **总交易次数**：所选时间段内的交易笔数
- **买入总额**：所有买入交易的金额总和
- **卖出总额**：所有卖出交易的金额总和
- **净流量**：卖出总额 - 买入总额（正数表示净流入）

### 行业汇总表
显示每个行业的：
- 标的数量：该行业有多少只股票
- 交易次数：该行业总交易笔数
- 买入/卖出总额
- 净流量

### 股票明细表
显示每只股票的：
- 所属行业
- 股票代码和公司名称
- 交易次数
- 买入/卖出数量
- 买入/卖出总额
- 净流量

## API 端点

### 1. 证券主档 API
```
GET  /api/v1/securities/              # 获取证券列表
POST /api/v1/securities/              # 创建证券（ADMIN）
GET  /api/v1/securities/{id}/         # 获取证券详情
PUT  /api/v1/securities/{id}/         # 更新证券（ADMIN）
```

### 2. 检查股票代码
```
GET /api/v1/securities/check-symbol/?project={project_id}&symbol={symbol}

返回示例：
{
  "exists": true,
  "security": {
    "id": 1,
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "asset_class": "US_STOCK",
    "asset_class_display": "美股",
    "sector": "科技",
    "exchange": "NASDAQ",
    "exchange_display": "NASDAQ"
  }
}
```

### 3. 交易汇总统计
```
GET /api/v1/securities/trade-summary/?project={id}&from={date}&to={date}&asset_class={class}&sector={sector}

参数：
- project: 项目ID（必填）
- from: 开始日期时间（可选）
- to: 结束日期时间（可选）
- asset_class: 资产类别筛选（US_STOCK/HK_STOCK/CRYPTO，可选）
- sector: 行业筛选（可选）

返回示例：
{
  "by_security": [
    {
      "asset_class": "US_STOCK",
      "asset_class_display": "美股",
      "sector": "科技",
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "trade_count": 5,
      "buy_total": 10000.00,
      "sell_total": 12000.00,
      "buy_quantity": 100,
      "sell_quantity": 100,
      "net_flow": 2000.00
    }
  ],
  "by_sector": [
    {
      "sector": "科技",
      "trade_count": 10,
      "buy_total": 50000.00,
      "sell_total": 55000.00,
      "net_flow": 5000.00,
      "symbol_count": 3
    }
  ]
}
```

### 4. 创建交易（增强版）
```
POST /api/v1/trades/

请求体（首次交易新标的）：
{
  "project": 1,
  "symbol": "BTC",
  "security_name": "Bitcoin",              # 首次需要
  "security_asset_class": "CRYPTO",        # 首次需要
  "security_sector": "加密货币",           # 首次可选
  "security_exchange": "BINANCE",          # 首次可选
  "side": "BUY",
  "price": 45000.00,
  "quantity": 1,
  "executed_at": "2025-12-27T10:30:00",
  "thesis": "看好比特币长期价值"
}

请求体（已存在股票）：
{
  "project": 1,
  "symbol": "AAPL",
  "side": "SELL",
  "price": 180.00,
  "quantity": 50,
  "executed_at": "2025-12-27T14:00:00",
  "thesis": "获利了结"
}
```

## 数据库模型

### Security 模型
```python
class Security(models.Model):
    """标的主档 (Security Master)"""
    ASSET_CLASS_CHOICES = [
        ('US_STOCK', '美股'),
        ('HK_STOCK', '港股'),
        ('CRYPTO', '加密货币'),
    ]
    
    EXCHANGE_CHOICES = [
        ('NASDAQ', 'NASDAQ'),
        ('NYSE', 'NYSE'),
        ('HKEX', 'HKEX'),
        ('BINANCE', 'Binance'),
        ('COINBASE', 'Coinbase'),
        ('OTHER', '其他'),
    ]
    
    project = ForeignKey(Project)          # 所属项目
    symbol = CharField(max_length=20)      # 标的代码（自动大写）
    name = CharField(max_length=200)       # 公司/资产全名
    asset_class = CharField(choices=ASSET_CLASS_CHOICES)  # 资产类别
    sector = CharField(max_length=100)     # 行业分类（可选）
    exchange = CharField(choices=EXCHANGE_CHOICES)        # 交易所（可选）
    created_by = ForeignKey(User)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['project', 'symbol']
```

### Trade 模型（增强版）
```python
class Trade(models.Model):
    project = ForeignKey(Project)
    security = ForeignKey(Security)        # 新增：关联证券主档
    symbol = CharField(max_length=20)      # 保留：便于快速查询
    side = CharField(choices=['BUY', 'SELL'])
    quantity = IntegerField()
    price = DecimalField()
    executed_at = DateTimeField()
    thesis = TextField()
    # ... 其他字段
```

## 权限控制

- **VIEWER（观察者）**：
  - 可查看证券列表
  - 可查看交易统计
  - 不可创建/编辑证券
  - 不可创建交易

- **ADMIN（管理员）**：
  - 所有 VIEWER 权限
  - 可创建交易并自动创建证券
  - 可编辑证券信息

## 注意事项

1. **标的代码规范**
   - 自动转换为大写
   - 美股建议使用 NASDAQ/NYSE 代码
   - 港股建议使用数字代码（如 00700）
   - 加密货币建议使用标准简称（如 BTC、ETH）

2. **资产类别选择**
   - **美股**：在美国交易所交易的股票
   - **港股**：在香港交易所交易的股票
   - **加密货币**：比特币、以太坊等数字货币

3. **行业分类建议**
   - 使用统一的行业分类标准
   - 便于后续统计分析
   - 可参考 GICS 行业分类

4. **首次录入**
   - 首次交易新标的时务必填写完整信息
   - 资产类别和名称为必填项
   - 后续交易将自动关联，无需重复填写

5. **数据一致性**
   - 每个项目内标的代码唯一
   - 修改标的信息会影响所有相关交易的显示

## 典型使用场景

### 场景 1：多资产组合分析
1. 按资产类别查看资金分布
2. 对比美股/港股/加密货币的表现
3. 评估资产配置合理性

### 场景 2：跨市场交易复盘
1. 选择特定资产类别（如美股）
2. 查看该类别下各标的交易表现
3. 计算该资产类别的整体盈亏

### 场景 3：行业轮动分析
1. 对比不同行业的净流量
2. 识别资金流向和热点板块
3. 调整投资策略

## 测试建议

1. **测试首次创建（美股）**：
   - 创建一笔 AAPL 的交易
   - 选择资产类别：美股
   - 填写公司名称、行业、交易所
   - 验证自动创建 Security

2. **测试首次创建（加密货币）**：
   - 创建一笔 BTC 的交易
   - 选择资产类别：加密货币
   - 填写名称 Bitcoin
   - 验证自动创建 Security

3. **测试自动关联**：
   - 再次交易 AAPL 或 BTC
   - 验证信息自动显示

4. **测试资产类别筛选**：
   - 创建多个资产类别的交易
   - 在复盘页面按资产类别筛选
   - 验证统计数据准确性

## 故障排查

### 问题 1：股票代码检测不工作
- 检查项目ID是否正确传递
- 查看浏览器控制台错误信息
- 确认 `/api/v1/securities/check-symbol/` 端点可访问

### 问题 2：统计数据不准确
- 确认时间范围参数格式正确（ISO 8601）
- 检查是否有 security 为空的交易记录
- 查看后端日志排查计算错误

### 问题 3：无法创建证券
- 确认用户角色为 ADMIN
- 检查股票代码是否已存在
- 验证必填字段是否完整

## 服务访问

- **服务端口**：20004
- **域名访问**：stocks.1plabs.pro
- **首页**：http://stocks.1plabs.pro/
- **分类复盘**：http://stocks.1plabs.pro/trades/analysis/?project={id}

## 更新日志

**版本 2.0.0**（2025-12-27）
- ✅ 新增资产类别字段（美股/港股/加密货币）
- ✅ 新增交易所字段
- ✅ 移除二级行业字段，简化为单一行业分类
- ✅ 交易表单支持资产类别选择
- ✅ 统计页面支持按资产类别筛选
- ✅ API 增强支持 asset_class 参数

**版本 1.0.0**（2025-12-27）
- ✅ 新增 Security 模型
- ✅ Trade 模型增加 security 外键
- ✅ 交易表单支持 Security 自动补全
- ✅ 新增分类复盘统计页面
- ✅ 新增 check-symbol 和 trade-summary API
- ✅ 项目 Dashboard 增加"分类复盘"入口
