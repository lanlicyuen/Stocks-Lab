from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404
from datetime import datetime
import json

from .models import (
    Trade, TradeAttachment, AuditLog, Security,
    MarketAccount, CashAdjustment
)
from .serializers import (
    TradeSerializer, TradeAttachmentSerializer, AuditLogSerializer, 
    UserSerializer, SecuritySerializer, MarketAccountSerializer, CashAdjustmentSerializer
)
from .permissions import IsOwner, IsAccountOwner, IsTradeOwner


def create_audit_log(action, model_type, model_id, user, changes=None):
    """创建审计日志"""
    AuditLog.objects.create(
        action=action,
        model_type=model_type,
        model_id=model_id,
        user=user,
        changes=json.dumps(changes, ensure_ascii=False) if changes else ''
    )


class MarketAccountViewSet(viewsets.ModelViewSet):
    """市场账户视图集 - 一级实体"""
    serializer_class = MarketAccountSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mode', 'market_type']
    
    def get_queryset(self):
        # 只返回用户自己的账户
        return MarketAccount.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        account = serializer.save(owner=self.request.user)
        create_audit_log('CREATE', 'MarketAccount', account.id, self.request.user, {
            'name': account.name,
            'mode': account.mode,
            'market_type': account.market_type
        })
    
    def perform_update(self, serializer):
        account = serializer.save()
        create_audit_log('UPDATE', 'MarketAccount', account.id, self.request.user, {
            'name': account.name
        })
    
    def perform_destroy(self, instance):
        create_audit_log('DELETE', 'MarketAccount', instance.id, self.request.user, {
            'name': instance.name
        })
        instance.delete()
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """获取账户完整汇总信息 - 支持做多/做空，只统计已成交交易"""
        from decimal import Decimal
        from collections import defaultdict
        
        account = self.get_object()
        serializer = self.get_serializer(account)
        
        # 获取所有已成交的交易（按交易时间和ID排序）
        filled_trades = account.trades.filter(status='FILLED').order_by('traded_at', 'id')
        
        # 1. 计算当前现金（按新规则）
        start_cash = Decimal(str(account.start_cash))
        
        # 资金调整
        adjustments_sum = account.adjustments.aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0')
        
        # 计算交易对现金的影响（只统计已成交的）
        cash_from_trades = sum(Decimal(str(t.cash_impact)) for t in filled_trades)
        
        # 计算冻结资金（待成交订单）
        pending_trades = account.trades.filter(status='PENDING')
        frozen_cash = sum(Decimal(str(t.frozen_cash)) for t in pending_trades)
        
        current_cash = start_cash + adjustments_sum + cash_from_trades
        available_cash = current_cash - frozen_cash
        
        # 2. 计算已实现盈亏（分多空持仓）
        positions = defaultdict(lambda: {
            'long_qty': Decimal('0'), 
            'long_cost': Decimal('0'),
            'short_qty': Decimal('0'),
            'short_cost': Decimal('0')
        })
        realized_pnl = Decimal('0')
        
        for trade in filled_trades:
            security_id = trade.security_id
            quantity = Decimal(str(trade.quantity))
            price = Decimal(str(trade.price))
            fee = Decimal(str(trade.fee))
            
            if trade.action == 'OPEN_LONG':
                # 开多：累加多头持仓和成本
                positions[security_id]['long_qty'] += quantity
                positions[security_id]['long_cost'] += quantity * price + fee
            
            elif trade.action == 'CLOSE_LONG':
                # 平多：计算多头已实现盈亏
                if positions[security_id]['long_qty'] > 0:
                    avg_cost = positions[security_id]['long_cost'] / positions[security_id]['long_qty']
                    realized_pnl += (price - avg_cost) * quantity - fee
                    
                    positions[security_id]['long_qty'] -= quantity
                    if positions[security_id]['long_qty'] > 0:
                        positions[security_id]['long_cost'] -= avg_cost * quantity
                    else:
                        positions[security_id]['long_cost'] = Decimal('0')
            
            elif trade.action == 'OPEN_SHORT':
                # 开空：累加空头持仓和成本
                positions[security_id]['short_qty'] += quantity
                positions[security_id]['short_cost'] += quantity * price - fee
            
            elif trade.action == 'CLOSE_SHORT':
                # 平空：计算空头已实现盈亏
                if positions[security_id]['short_qty'] > 0:
                    avg_cost = positions[security_id]['short_cost'] / positions[security_id]['short_qty']
                    realized_pnl += (avg_cost - price) * quantity - fee
                    
                    positions[security_id]['short_qty'] -= quantity
                    if positions[security_id]['short_qty'] > 0:
                        positions[security_id]['short_cost'] -= avg_cost * quantity
                    else:
                        positions[security_id]['short_cost'] = Decimal('0')
        
        # 3. 统计数据（只统计已成交的）
        total_fees = filled_trades.aggregate(total=Sum('fee'))['total'] or Decimal('0')
        
        # 4. 回报率计算
        if start_cash > 0:
            return_pct = (realized_pnl / start_cash) * Decimal('100')
        else:
            return_pct = Decimal('0')
        
        # 构建返回数据
        data = serializer.data
        data['current_cash'] = float(current_cash)
        data['available_cash'] = float(available_cash)
        data['frozen_cash'] = float(frozen_cash)
        data['realized_pnl'] = float(realized_pnl)
        data['return_pct'] = float(return_pct)
        
        data['summary'] = {
            'securities_count': account.securities.count(),
            'trade_count': filled_trades.count(),
            'pending_count': pending_trades.count(),
            'open_long_count': filled_trades.filter(action='OPEN_LONG').count(),
            'close_long_count': filled_trades.filter(action='CLOSE_LONG').count(),
            'open_short_count': filled_trades.filter(action='OPEN_SHORT').count(),
            'close_short_count': filled_trades.filter(action='CLOSE_SHORT').count(),
            'total_fees': str(total_fees),
        }
        
        # 5. 添加持仓信息
        positions_list = []
        for security_id, pos in positions.items():
            if pos['long_qty'] > 0 or pos['short_qty'] > 0:
                security = account.securities.filter(id=security_id).first()
                if security:
                    position_data = {
                        'security_id': security_id,
                        'symbol': security.symbol,
                        'name': security.name,
                    }
                    if pos['long_qty'] > 0:
                        position_data['long_quantity'] = float(pos['long_qty'])
                        position_data['long_avg_cost'] = float(pos['long_cost'] / pos['long_qty'])
                    if pos['short_qty'] > 0:
                        position_data['short_quantity'] = float(pos['short_qty'])
                        position_data['short_avg_cost'] = float(pos['short_cost'] / pos['short_qty'])
                    positions_list.append(position_data)
        
        data['positions'] = positions_list
        
        return Response(data)
    
    @action(detail=True, methods=['get'])
    def trades(self, request, pk=None):
        """获取账户的交易列表"""
        account = self.get_object()
        trades = account.trades.all()
        serializer = TradeSerializer(trades, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def adjustments(self, request, pk=None):
        """获取账户的资金调整列表"""
        account = self.get_object()
        adjustments = account.adjustments.all()
        serializer = CashAdjustmentSerializer(adjustments, many=True)
        return Response(serializer.data)


class SecurityViewSet(viewsets.ModelViewSet):
    """标的主档视图集"""
    serializer_class = SecuritySerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['account', 'asset_type', 'sector']
    
    def get_queryset(self):
        # 只返回用户自己账户下的标的
        return Security.objects.filter(account__owner=self.request.user)
    
    def perform_create(self, serializer):
        # 安全检查：确保用户只能在自己的账户下创建标的
        account_id = self.request.data.get('account')
        if account_id:
            account = get_object_or_404(MarketAccount, id=account_id, owner=self.request.user)
            security = serializer.save(account=account)
        else:
            security = serializer.save()
        
        create_audit_log('CREATE', 'Security', security.id, self.request.user, {
            'symbol': security.symbol,
            'name': security.name
        })
    
    def perform_update(self, serializer):
        # 安全检查：确保用户只能更新自己账户下的标的
        security = serializer.save()
        create_audit_log('UPDATE', 'Security', security.id, self.request.user, {
            'symbol': security.symbol,
            'name': security.name
        })
    
    def perform_destroy(self, instance):
        # 记录删除前的信息
        create_audit_log('DELETE', 'Security', instance.id, self.request.user, {
            'symbol': instance.symbol,
            'name': instance.name
        })
        instance.delete()


class TradeViewSet(viewsets.ModelViewSet):
    """交易记录视图集"""
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['account', 'security', 'action', 'status']
    
    def get_queryset(self):
        # 只返回用户自己账户下的交易
        return Trade.objects.filter(account__owner=self.request.user)
    
    def perform_create(self, serializer):
        from decimal import Decimal
        from collections import defaultdict
        from rest_framework.exceptions import ValidationError
        
        # 安全检查：确保用户只能在自己的账户下创建交易
        account_id = self.request.data.get('account')
        if account_id:
            account = get_object_or_404(MarketAccount, id=account_id, owner=self.request.user)
        else:
            raise ValidationError({'account': '必须指定账户'})
        
        # 持仓验证
        action = self.request.data.get('action')
        security_id = self.request.data.get('security')
        quantity = Decimal(str(self.request.data.get('quantity', 0)))
        
        if action in ['CLOSE_LONG', 'CLOSE_SHORT'] and quantity > 0:
            # 计算当前持仓（分多空，只统计已成交的）
            trades = account.trades.filter(security_id=security_id, status='FILLED').order_by('traded_at', 'id')
            long_position = Decimal('0')
            short_position = Decimal('0')
            
            for t in trades:
                qty = Decimal(str(t.quantity))
                if t.action == 'OPEN_LONG':
                    long_position += qty
                elif t.action == 'CLOSE_LONG':
                    long_position -= qty
                elif t.action == 'OPEN_SHORT':
                    short_position += qty
                elif t.action == 'CLOSE_SHORT':
                    short_position -= qty
            
            # 检查持仓是否足够
            if action == 'CLOSE_LONG' and long_position < quantity:
                security = Security.objects.get(id=security_id)
                raise ValidationError({
                    'quantity': f'{security.symbol} 多头持仓不足。当前多头持仓: {long_position}，尝试平多: {quantity}'
                })
            elif action == 'CLOSE_SHORT' and short_position < quantity:
                security = Security.objects.get(id=security_id)
                raise ValidationError({
                    'quantity': f'{security.symbol} 空头持仓不足。当前空头持仓: {short_position}，尝试平空: {quantity}'
                })
        
        trade = serializer.save()
        create_audit_log('CREATE', 'Trade', trade.id, self.request.user, {
            'security': trade.security.symbol,
            'action': trade.action,
            'quantity': str(trade.quantity),
            'price': str(trade.price)
        })
    
    def perform_update(self, serializer):
        trade = serializer.save()
        create_audit_log('UPDATE', 'Trade', trade.id, self.request.user, {
            'security': trade.security.symbol
        })
    
    def perform_destroy(self, instance):
        create_audit_log('DELETE', 'Trade', instance.id, self.request.user, {
            'security': instance.security.symbol
        })
        instance.delete()
    
    @action(detail=True, methods=['post'])
    def fill(self, request, pk=None):
        """确认成交订单"""
        from django.utils import timezone
        
        trade = self.get_object()
        
        if trade.status != 'PENDING':
            return Response(
                {'error': '只能确认待成交订单', 'status': trade.status},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        trade.status = 'FILLED'
        trade.filled_at = timezone.now()
        trade.save()
        
        create_audit_log('UPDATE', 'Trade', trade.id, request.user, {
            'action': '确认成交',
            'status': trade.status
        })
        
        serializer = self.get_serializer(trade)
        return Response(serializer.data)
    
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
        
        serializer = self.get_serializer(trade)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def close_position(self, request):
        """平仓操作 - 直接创建平仓交易并成交"""
        from django.utils import timezone
        from decimal import Decimal
        
        account_id = request.data.get('account')
        security_id = request.data.get('security')
        close_price = request.data.get('close_price')
        position_type = request.data.get('position_type')  # 'long' or 'short'
        quantity = request.data.get('quantity')
        notes = request.data.get('notes', '')
        
        if not all([account_id, security_id, close_price, position_type, quantity]):
            return Response(
                {'error': '缺少必要参数: account, security, close_price, position_type, quantity'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 权限检查
        account = get_object_or_404(MarketAccount, id=account_id, owner=request.user)
        
        # 创建平仓交易
        action = 'CLOSE_LONG' if position_type == 'long' else 'CLOSE_SHORT'
        
        trade = Trade.objects.create(
            account=account,
            security_id=security_id,
            action=action,
            status='FILLED',  # 平仓直接成交
            quantity=Decimal(str(quantity)),
            price=Decimal(str(close_price)),
            fee=Decimal('0'),  # 可以根据需要计算手续费
            traded_at=timezone.now(),
            filled_at=timezone.now(),
            notes=notes or f'平仓操作'
        )
        
        create_audit_log('CREATE', 'Trade', trade.id, request.user, {
            'action': '平仓',
            'position_type': position_type,
            'quantity': str(quantity),
            'price': str(close_price)
        })
        
        serializer = self.get_serializer(trade)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CashAdjustmentViewSet(viewsets.ModelViewSet):
    """资金调整视图集"""
    serializer_class = CashAdjustmentSerializer
    permission_classes = [IsAuthenticated, IsAccountOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['account', 'date']
    
    def get_queryset(self):
        # 只返回用户自己账户下的调整记录
        return CashAdjustment.objects.filter(account__owner=self.request.user)
    
    def perform_create(self, serializer):
        # 安全检查：确保用户只能在自己的账户下创建资金调整
        account_id = self.request.data.get('account')
        if account_id:
            account = get_object_or_404(MarketAccount, id=account_id, owner=self.request.user)
        
        adjustment = serializer.save()
        create_audit_log('CREATE', 'CashAdjustment', adjustment.id, self.request.user, {
            'amount': str(adjustment.amount),
            'reason': adjustment.reason
        })


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """审计日志视图集（只读）"""
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['model_type', 'action']
    
    def get_queryset(self):
        # 只返回用户自己的操作日志
        return AuditLog.objects.filter(user=self.request.user)


class TradeAttachmentViewSet(viewsets.ModelViewSet):
    """交易附件视图集 - 支持 multipart 上传"""
    serializer_class = TradeAttachmentSerializer
    permission_classes = [IsAuthenticated, IsTradeOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['trade']
    
    def get_queryset(self):
        # 只返回用户自己交易的附件
        return TradeAttachment.objects.filter(trade__account__owner=self.request.user)
    
    def perform_create(self, serializer):
        # 安全检查：确保用户只能给自己的交易上传附件
        trade_id = self.request.data.get('trade')
        if trade_id:
            trade = get_object_or_404(Trade, id=trade_id, account__owner=self.request.user)
        
        attachment = serializer.save()
        create_audit_log('CREATE', 'TradeAttachment', attachment.id, self.request.user, {
            'trade_id': attachment.trade.id,
            'file_type': attachment.file_type
        })
