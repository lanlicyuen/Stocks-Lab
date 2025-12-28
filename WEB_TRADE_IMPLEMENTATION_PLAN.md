# 网页版交易闭环实施计划

## 📋 修改文件清单

### ✅ 已完成
1. **core/models.py** - Trade 模型
   - ✅ quantity: IntegerField → DecimalField (支持小数)
   - ✅ thesis/review → notes (统一备注字段)
   - ✅ 添加 save() 方法自动转换 symbol 为大写
   - ✅ 添加 total_cost 属性
   - ✅ 更新 ordering: 按 executed_at 和 id 排序

2. **core/serializers.py** - TradeSerializer
   - ✅ 更新字段名: thesis_html/review_html → notes_html
   - ✅ 添加 total_cost, side_display 字段
   - ✅ 删除废弃的 get_thesis_html/get_review_html 方法

### ⏳ 待实施

#### 后端文件

3. **core/viewsets.py** - 计算逻辑 (CRITICAL)
   ```python
   # TradeViewSet
   - perform_create(): 添加持仓验证（SELL 时）
   - 计算 realized_pnl（平均成本法）
   
   # MarketAccountViewSet.summary()
   - 重写 current_cash 计算公式
   - 添加 realized_pnl 计算
   - 返回: current_cash, realized_pnl, total_fee, buy_count, sell_count, trade_count
   ```

4. **core/admin.py** - 更新 Trade 管理界面
   ```python
   # TradeAdmin
   - 更新 list_display: 使用 notes 替代 thesis
   - 更新 search_fields
   ```

#### 前端页面

5. **templates/trade_form.html** (NEW) - 新增交易表单
   ```
   字段:
   - symbol (自动大写)
   - side (BUY/SELL 单选)
   - quantity (decimal)
   - price (decimal)
   - fee (默认0)
   - executed_at (datetime-local)
   - notes (textarea, Markdown)
   - attachments (多文件上传, 可选)
   
   提交: POST /api/v1/trades/
   成功后: 跳转到 /accounts/{id}/
   ```

6. **templates/account_detail.html** (UPDATE) - 账户详情页
   ```
   添加:
   - "新增交易" 按钮 → trade_form.html
   - 最近交易列表 (表格显示)
   - 空态文案: "还没有交易记录，点击新增第一笔交易"
   - 资金统计卡片: 使用新的 summary API
   
   更新:
   - 调用 /api/v1/accounts/{id}/summary/ 获取数据
   - 展示 current_cash, realized_pnl, buy/sell counts
   ```

7. **templates/adjustment_form.html** (NEW) - 资金调整表单
   ```
   字段:
   - date
   - amount (正数入金，负数出金)
   - reason (textarea)
   - attachment (可选)
   
   提交: POST /api/v1/cash-adjustments/
   ```

8. **templates/accounts_list.html** (UPDATE) - 账户列表
   ```
   - 每个账户添加 "查看详情" 链接 → /accounts/{id}/
   ```

#### URL 路由

9. **stocks_lab/urls.py** (UPDATE)
   ```python
   urlpatterns = [
       path('accounts/<int:account_id>/', views.account_detail, name='account_detail'),
       path('accounts/<int:account_id>/trades/new/', views.trade_form, name='trade_form'),
       path('accounts/<int:account_id>/adjustments/new/', views.adjustment_form, name='adjustment_form'),
   ]
   ```

10. **core/views.py** (NEW or UPDATE)
    ```python
    def account_detail(request, account_id):
        # 渲染 account_detail.html
    
    def trade_form(request, account_id):
        # 渲染 trade_form.html
    
    def adjustment_form(request, account_id):
        # 渲染 adjustment_form.html
    ```

---

## 🔢 计算公式

### Current Cash
```python
current_cash = start_cash 
             + sum(adjustments.amount)
             + sum(SELL trades: quantity * price - fee)
             - sum(BUY trades: quantity * price + fee)
```

### Realized PnL (平均成本法)
```python
# 按 executed_at + id 顺序回放所有交易
positions = {}  # {symbol: {'quantity': 0, 'total_cost': 0}}

for trade in trades.order_by('executed_at', 'id'):
    if trade.side == 'BUY':
        positions[symbol]['quantity'] += trade.quantity
        positions[symbol]['total_cost'] += (trade.quantity * trade.price + trade.fee)
    elif trade.side == 'SELL':
        if positions[symbol]['quantity'] < trade.quantity:
            # 持仓不足，返回 400 错误
            raise ValidationError(f"{symbol} 持仓不足")
        
        avg_cost = positions[symbol]['total_cost'] / positions[symbol]['quantity']
        realized_pnl += (trade.price - avg_cost) * trade.quantity - trade.fee
        
        positions[symbol]['quantity'] -= trade.quantity
        positions[symbol]['total_cost'] -= avg_cost * trade.quantity
```

---

## 🔐 权限控制 (Viewer Role)

### 方案: 使用 Django 内置 Permission 系统

```python
# core/permissions.py (UPDATE)
class IsAccountOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Viewer 可以读取
            return obj.account.owner == request.user
        
        # 写操作需要是 owner 且有权限
        if obj.account.owner != request.user:
            return False
        
        # 检查用户是否有 change_trade 权限
        return request.user.has_perm('core.add_trade')

# 前端: 根据权限隐藏按钮
{% if perms.core.add_trade %}
<button>新增交易</button>
{% endif %}
```

### 简化方案 (P0):
- 暂时不实现 viewer 角色
- 所有 owner 都有完整权限
- 在 P1 阶段再添加角色系统

---

## 📝 数据库迁移

```bash
cd /home/lanlic/Html-Project/Stocks-Lab
source venv/bin/activate

# 创建迁移文件
python manage.py makemigrations core

# 预览迁移 SQL
python manage.py sqlmigrate core 0003

# 执行迁移
python manage.py migrate

# 检查迁移状态
python manage.py showmigrations core
```

### 预期迁移内容
```sql
-- 修改 quantity 字段类型
ALTER TABLE core_trade ALTER COLUMN quantity TYPE DECIMAL(15,4);

-- 重命名字段
ALTER TABLE core_trade RENAME COLUMN thesis TO notes;
ALTER TABLE core_trade DROP COLUMN review;

-- 更新索引
CREATE INDEX core_trade_account_executed_at ON core_trade (account_id, executed_at DESC);
```

---

## 🧪 测试清单

### 后端测试
- [ ] POST /api/v1/trades/ 创建交易
- [ ] 持仓不足时返回 400
- [ ] GET /api/v1/accounts/{id}/summary/ 返回正确的 current_cash
- [ ] realized_pnl 计算正确

### 前端测试
- [ ] 访问 /accounts/{id}/ 显示详情页
- [ ] 点击"新增交易"按钮跳转到表单
- [ ] 填写表单并提交成功
- [ ] 提交后跳回详情页并刷新数据
- [ ] 空态文案显示正常

---

## 🚀 实施顺序

### Phase 1: 数据库和 API (优先)
1. ✅ 更新 Trade 模型
2. ✅ 更新 TradeSerializer
3. ⏳ 更新 TradeViewSet (持仓验证)
4. ⏳ 重写 MarketAccountViewSet.summary()
5. ⏳ 数据库迁移

### Phase 2: 前端页面
6. ⏳ 创建 trade_form.html
7. ⏳ 更新 account_detail.html
8. ⏳ 创建 adjustment_form.html
9. ⏳ 添加 URL 路由
10. ⏳ 创建 view 函数

### Phase 3: 测试和优化
11. ⏳ 端到端测试
12. ⏳ 错误处理优化
13. ⏳ UI/UX 优化

---

## ⚠️ 注意事项

1. **数据迁移风险**: thesis → notes 字段重命名会保留数据
2. **quantity 类型变更**: IntegerField → DecimalField 兼容现有数据
3. **持仓验证**: SELL 时必须检查持仓，避免负数
4. **时区处理**: executed_at 需要正确处理时区
5. **文件上传**: attachments 需要配置 MEDIA_ROOT 和 MEDIA_URL

---

继续实施？请确认是否开始 Phase 1 的剩余步骤。
