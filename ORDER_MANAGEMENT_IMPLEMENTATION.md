# 订单管理系统实现指南

## ✅ 已完成

### 1. 数据库层
- ✅ Trade模型添加`status`字段（PENDING/FILLED/CANCELLED）
- ✅ Trade模型添加`filled_at`字段（成交时间）
- ✅ 添加`frozen_cash`属性（计算冻结资金）
- ✅ 修改`cash_impact`属性（只有FILLED状态才影响现金）
- ✅ 创建并应用迁移0006
- ✅ 现有交易标记为已成交

## 📝 待实现步骤

### 2. 序列化器更新 (core/serializers.py)
在TradeSerializer中添加status和filled_at字段：
```python
class TradeSerializer(serializers.ModelSerializer):
    # ... 现有代码 ...
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Trade
        fields = [
            'id', 'account', 'account_info', 'security', 'security_info',
            'action', 'action_display', 'status', 'status_display',
            'quantity', 'price', 'fee', 'traded_at', 'filled_at',
            'notes', 'notes_html', 'total_amount', 'cash_impact',
            'created_at', 'updated_at', 'attachments', 'attachments_count'
        ]
        read_only_fields = ['id', 'total_amount', 'cash_impact', 'created_at', 'updated_at']
```

### 3. ViewSets更新 (core/viewsets.py)
添加三个自定义action：

```python
class TradeViewSet(viewsets.ModelViewSet):
    # ... 现有代码 ...
    
    @action(detail=True, methods=['post'])
    def fill(self, request, pk=None):
        """确认成交订单"""
        trade = self.get_object()
        
        if trade.status != 'PENDING':
            return Response(
                {'error': '只能确认待成交订单'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        trade.status = 'FILLED'
        trade.filled_at = timezone.now()
        trade.save()
        
        create_audit_log('UPDATE', 'Trade', trade.id, request.user, {
            'action': '确认成交',
            'status': trade.status
        })
        
        return Response({'message': '订单已成交'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消订单"""
        trade = self.get_object()
        
        if trade.status != 'PENDING':
            return Response(
                {'error': '只能取消待成交订单'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        trade.status = 'CANCELLED'
        trade.save()
        
        create_audit_log('UPDATE', 'Trade', trade.id, request.user, {
            'action': '取消订单',
            'status': trade.status
        })
        
        return Response({'message': '订单已取消'})
    
    @action(detail=False, methods=['post'])
    def close_position(self, request):
        """平仓操作"""
        account_id = request.data.get('account')
        security_id = request.data.get('security')
        close_price = request.data.get('close_price')
        position_type = request.data.get('position_type')  # 'long' or 'short'
        quantity = request.data.get('quantity')
        
        if not all([account_id, security_id, close_price, position_type, quantity]):
            return Response(
                {'error': '缺少必要参数'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 创建平仓交易
        action = 'CLOSE_LONG' if position_type == 'long' else 'CLOSE_SHORT'
        
        trade = Trade.objects.create(
            account_id=account_id,
            security_id=security_id,
            action=action,
            status='FILLED',  # 平仓直接成交
            quantity=quantity,
            price=close_price,
            fee=0,  # 可以根据需要计算手续费
            traded_at=timezone.now(),
            filled_at=timezone.now(),
            notes=f'平仓操作'
        )
        
        serializer = self.get_serializer(trade)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

### 4. 修改账户summary计算 (core/viewsets.py MarketAccountViewSet.summary)
只统计FILLED状态的交易：
```python
def summary(self, request, pk=None):
    # ...
    # 将所有 account.trades.all() 改为:
    filled_trades = account.trades.filter(status='FILLED')
    
    # 统计时也要过滤:
    summary = {
        'trade_count': filled_trades.count(),
        'open_long_count': filled_trades.filter(action='OPEN_LONG').count(),
        'close_long_count': filled_trades.filter(action='CLOSE_LONG').count(),
        'open_short_count': filled_trades.filter(action='OPEN_SHORT').count(),
        'close_short_count': filled_trades.filter(action='CLOSE_SHORT').count(),
        'total_fees': sum(float(t.fee) for t in filled_trades),
    }
```

### 5. 前端页面更新 (templates/account_detail.html)

#### 5.1 添加待成交订单卡片（在"当前持仓"之前）
```html
<!-- Pending Orders -->
<div class="card">
    <div class="card-header">
        <h2 class="card-title">⏳ 待成交订单</h2>
    </div>
    <div class="card-body">
        <div id="pendingOrders">
            <div class="loading">
                <div class="spinner"></div>
                <div>加载中...</div>
            </div>
        </div>
    </div>
</div>
```

#### 5.2 修改持仓卡片，添加平仓按钮
在loadPositions函数中添加平仓按钮：
```javascript
// 在每个持仓卡片底部添加:
<button class="btn btn-warning btn-sm" style="width: 100%; margin-top: 10px;" 
        onclick="showClosePositionModal('${pos.security_id}', 'long', ${pos.long_quantity}, ${pos.long_avg_cost})">
    📤 平仓
</button>
```

#### 5.3 添加JavaScript函数
```javascript
// 加载待成交订单
async function loadPendingOrders() {
    try {
        const response = await API.get(`/trades/?account=${accountId}&status=PENDING&ordering=-created_at`);
        const orders = response.results || response;
        
        if (orders.length === 0) {
            document.getElementById('pendingOrders').innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">✅</div>
                    <div>暂无待成交订单</div>
                </div>
            `;
            return;
        }
        
        document.getElementById('pendingOrders').innerHTML = orders.map(order => `
            <div class="mobile-card" style="border-left: 3px solid #ffc107;">
                <div class="mobile-card-primary">
                    <span>${order.security_info.symbol}</span>
                    <span class="badge" style="background: #ffc107; color: #333;">
                        ⏳ ${order.action_display}
                    </span>
                </div>
                <div class="mobile-card-row">
                    <span class="mobile-card-label">数量</span>
                    <span class="mobile-card-value">${order.quantity}</span>
                </div>
                <div class="mobile-card-row">
                    <span class="mobile-card-label">价格</span>
                    <span class="mobile-card-value">${formatCurrency(order.price)}</span>
                </div>
                <div class="mobile-card-row">
                    <span class="mobile-card-label">创建时间</span>
                    <span class="mobile-card-value">${new Date(order.created_at).toLocaleString('zh-CN')}</span>
                </div>
                <div style="display: flex; gap: 10px; margin-top: 10px;">
                    <button class="btn btn-success btn-sm" style="flex: 1;" onclick="fillOrder(${order.id})">
                        ✅ 确认成交
                    </button>
                    <button class="btn btn-secondary btn-sm" style="flex: 1;" onclick="cancelOrder(${order.id})">
                        ❌ 取消
                    </button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to load pending orders:', error);
        document.getElementById('pendingOrders').innerHTML = '<div class="empty-state">加载失败</div>';
    }
}

// 确认成交
async function fillOrder(tradeId) {
    if (!confirm('确认成交此订单？成交后将扣除资金并生成持仓。')) return;
    
    try {
        await API.post(`/trades/${tradeId}/fill/`);
        showSuccess('订单已成交！');
        await loadAccountDetails();
        await loadPendingOrders();
    } catch (error) {
        showError('成交失败：' + (error.message || '请重试'));
    }
}

// 取消订单
async function cancelOrder(tradeId) {
    if (!confirm('确认取消此订单？取消后将释放冻结资金。')) return;
    
    try {
        await API.post(`/trades/${tradeId}/cancel/`);
        showSuccess('订单已取消');
        await loadPendingOrders();
    } catch (error) {
        showError('取消失败：' + (error.message || '请重试'));
    }
}

// 显示平仓弹窗
function showClosePositionModal(securityId, positionType, quantity, avgCost) {
    // TODO: 创建平仓弹窗HTML和逻辑
}
```

#### 5.4 在loadAccountDetails中添加加载待成交订单
```javascript
await Promise.all([
    loadPositions(accountData.positions || []),
    loadTradeRecords(),
    loadPendingOrders()  // 添加这行
]);
```

## 🎯 下一步
1. 更新TradeSerializer添加status字段
2. 更新TradeViewSet添加fill/cancel/close_position三个action
3. 修改summary计算只统计FILLED交易
4. 前端添加待成交订单显示
5. 前端添加持仓平仓功能
6. 创建平仓弹窗和逻辑

需要我继续实现吗？
