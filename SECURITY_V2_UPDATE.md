# Security Master v2.0 更新说明

## 🎯 核心变更

### 新增功能

1. **资产类别分类**
   - ✅ 新增 `asset_class` 字段（美股/港股/加密货币）
   - ✅ 每个标的必须指定资产类别
   - ✅ 支持按资产类别筛选统计

2. **交易所信息**
   - ✅ 新增 `exchange` 字段（NASDAQ/NYSE/HKEX/Binance等）
   - ✅ 可选字段，用于记录标的交易场所

3. **简化行业分类**
   - ✅ 移除 `industry`（二级行业）字段
   - ✅ 保留 `sector`（一级行业）字段，改为可选

### 界面优化

1. **交易表单**
   - 新增资产类别选择下拉框（必填）
   - 公司/资产全名输入框（必填）
   - 行业分类改为可选
   - 新增交易所选择下拉框（可选）

2. **分类复盘页面**
   - 新增资产类别筛选器
   - 股票明细表显示资产类别徽章
   - 支持跨资产类别统计

### API 增强

1. **SecuritySerializer**
   - 新增 `asset_class` 和 `asset_class_display` 字段
   - 新增 `exchange` 和 `exchange_display` 字段
   - 移除 `industry` 字段

2. **TradeSerializer**
   - 创建交易时支持传入 `security_asset_class`（首次必需）
   - 创建交易时支持传入 `security_exchange`（首次可选）
   - 移除 `security_industry` 参数

3. **trade-summary API**
   - 新增 `asset_class` 查询参数
   - 返回数据包含 `asset_class` 和 `asset_class_display`

## 📊 数据库变更

### Migration: 0003_alter_security_options_remove_security_industry_and_more

```sql
-- 移除字段
ALTER TABLE core_security DROP COLUMN industry;

-- 新增字段
ALTER TABLE core_security ADD COLUMN asset_class VARCHAR(20) NOT NULL DEFAULT 'US_STOCK';
ALTER TABLE core_security ADD COLUMN exchange VARCHAR(20) DEFAULT '';

-- 修改字段
ALTER TABLE core_security MODIFY COLUMN sector VARCHAR(100) DEFAULT '';

-- 新增索引
CREATE INDEX core_securi_project_4bdf25_idx ON core_security (project_id, asset_class);
```

### 数据迁移策略

- **现有数据处理**：所有现有 Security 记录的 `asset_class` 默认设为 `US_STOCK`
- **字段变更**：`industry` 字段已删除，相关数据需手动迁移（如需要）
- **兼容性**：旧交易记录仍可正常显示，但建议更新关联的 Security 信息

## 🔄 迁移指南

### 对于已有数据

1. **检查现有 Security 记录**
   ```bash
   cd /home/lanlic/Html-Project/Stocks-Lab
   source venv/bin/activate
   python manage.py shell
   ```
   ```python
   from core.models import Security
   # 查看所有现有记录
   for sec in Security.objects.all():
       print(f"{sec.symbol}: {sec.asset_class} - {sec.name}")
   ```

2. **更新资产类别**（如需要）
   ```python
   # 将港股标的更新为 HK_STOCK
   Security.objects.filter(symbol__startswith='0').update(asset_class='HK_STOCK')
   
   # 将加密货币标的更新为 CRYPTO
   Security.objects.filter(symbol__in=['BTC', 'ETH']).update(asset_class='CRYPTO')
   ```

3. **添加交易所信息**（可选）
   ```python
   Security.objects.filter(asset_class='US_STOCK').update(exchange='NASDAQ')
   Security.objects.filter(asset_class='HK_STOCK').update(exchange='HKEX')
   Security.objects.filter(asset_class='CRYPTO').update(exchange='BINANCE')
   ```

### 对于新数据

- 首次创建交易时，必须选择资产类别
- 建议填写交易所信息，便于后续分析
- 行业分类改为可选，可根据需要填写

## 🎨 前端变更对比

### 交易表单（trade_form_new.html）

**旧版本**：
```html
<input id="securityNameInput" placeholder="公司全名（必填）">
<input id="securitySectorInput" placeholder="行业分类（必填）">
<input id="securityIndustryInput" placeholder="二级行业（可选）">
```

**新版本**：
```html
<select id="securityAssetClassInput" required>
  <option value="US_STOCK">美股</option>
  <option value="HK_STOCK">港股</option>
  <option value="CRYPTO">加密货币</option>
</select>
<input id="securityNameInput" placeholder="公司/资产全名（必填）">
<input id="securitySectorInput" placeholder="行业分类（可选）">
<select id="securityExchangeInput">
  <option value="NASDAQ">NASDAQ</option>
  <option value="NYSE">NYSE</option>
  <option value="HKEX">HKEX</option>
  <option value="BINANCE">Binance</option>
</select>
```

### 分类复盘页面（trade_analysis_new.html）

**新增筛选器**：
```html
<select id="assetClassFilter">
  <option value="">全部类别</option>
  <option value="US_STOCK">美股</option>
  <option value="HK_STOCK">港股</option>
  <option value="CRYPTO">加密货币</option>
</select>
```

**表格显示优化**：
```html
<td>
  <span class="badge badge-primary">美股</span>
  <span class="badge badge-success">港股</span>
  <span class="badge badge-warning">加密货币</span>
</td>
```

## 🚀 使用示例

### 示例 1：创建美股交易

```javascript
// 用户输入 AAPL
// 系统检测不存在，展开表单
{
  "symbol": "AAPL",
  "security_asset_class": "US_STOCK",      // 必选
  "security_name": "Apple Inc.",           // 必填
  "security_sector": "科技",               // 可选
  "security_exchange": "NASDAQ",           // 可选
  // ... 其他交易字段
}
```

### 示例 2：创建港股交易

```javascript
// 用户输入 00700
{
  "symbol": "00700",
  "security_asset_class": "HK_STOCK",      // 必选
  "security_name": "腾讯控股",             // 必填
  "security_sector": "科技",               // 可选
  "security_exchange": "HKEX",             // 可选
  // ... 其他交易字段
}
```

### 示例 3：创建加密货币交易

```javascript
// 用户输入 BTC
{
  "symbol": "BTC",
  "security_asset_class": "CRYPTO",        // 必选
  "security_name": "Bitcoin",              // 必填
  "security_sector": "加密货币",           // 可选
  "security_exchange": "BINANCE",          // 可选
  // ... 其他交易字段
}
```

### 示例 4：按资产类别统计

```
GET /api/v1/securities/trade-summary/?project=1&asset_class=US_STOCK

返回美股交易统计：
{
  "by_security": [
    {
      "asset_class": "US_STOCK",
      "asset_class_display": "美股",
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "trade_count": 10,
      "buy_total": 50000,
      "sell_total": 55000,
      "net_flow": 5000
    }
  ]
}
```

## ✅ 验证清单

- [x] 数据库迁移成功执行
- [x] 现有 Security 记录保留并设置默认 asset_class
- [x] 交易表单显示资产类别选择器
- [x] 首次创建交易时必须选择资产类别
- [x] 再次交易时自动显示完整标的信息
- [x] 分类复盘页面支持资产类别筛选
- [x] API 返回包含 asset_class 信息
- [x] 服务正常运行

## 📝 注意事项

1. **必填字段变更**
   - 旧版：公司名 + 行业分类为必填
   - 新版：资产类别 + 公司名为必填，行业改为可选

2. **数据兼容性**
   - 现有数据的 asset_class 默认为 US_STOCK
   - 如需更准确分类，请手动更新
   - 旧数据的 industry 字段已被移除

3. **前端行为变更**
   - 首次交易时必须选择资产类别
   - 资产类别选择会影响后续筛选和统计
   - 建议为每个标的选择准确的资产类别

4. **API 调用更新**
   - 创建交易时需传入 `security_asset_class`
   - 统计 API 支持 `asset_class` 查询参数
   - 返回数据包含 `asset_class_display` 字段

## 🔗 相关文档

- [SECURITY_FEATURE_GUIDE.md](SECURITY_FEATURE_GUIDE.md) - 完整功能使用指南
- [SECURITY_QUICK_REF.md](SECURITY_QUICK_REF.md) - 快速参考卡片
- [test_security_feature.sh](test_security_feature.sh) - 自动化测试脚本

## 📞 技术支持

如遇到问题，请检查：
1. 数据库迁移是否成功执行
2. 服务是否正常运行（端口 20004）
3. 前端 JavaScript 控制台是否有错误
4. API 返回数据格式是否正确

---

**版本**: 2.0.0  
**发布日期**: 2025-12-27  
**服务地址**: http://stocks.1plabs.pro/
