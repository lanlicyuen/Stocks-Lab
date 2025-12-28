from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Trade, TradeAttachment, AuditLog, Security,
    MarketAccount, CashAdjustment
)
from django.db.models import Sum, Q
import markdown


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class SecuritySerializer(serializers.ModelSerializer):
    """标的主档序列化器"""
    trade_count = serializers.SerializerMethodField()
    asset_type_display = serializers.CharField(source='get_asset_type_display', read_only=True)
    
    class Meta:
        model = Security
        fields = [
            'id', 'account', 'symbol', 'name', 'asset_type', 'asset_type_display',
            'sector', 'created_at', 'updated_at', 'trade_count'
        ]
        read_only_fields = ['id', 'account', 'created_at', 'updated_at']
    
    def get_trade_count(self, obj):
        return obj.trades.count()


class TradeAttachmentSerializer(serializers.ModelSerializer):
    """交易附件序列化器 - 移动端友好"""
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = TradeAttachment
        fields = [
            'id', 'trade', 'file', 'file_url', 'file_type', 
            'file_size', 'description', 'uploaded_at'
        ]
        read_only_fields = ['id', 'file_type', 'file_size', 'uploaded_at']
    
    def get_file_url(self, obj):
        """返回完整的文件 URL"""
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class TradeSerializer(serializers.ModelSerializer):
    """交易记录序列化器"""
    security_info = SecuritySerializer(source='security', read_only=True)
    account_info = serializers.SerializerMethodField()
    attachments = TradeAttachmentSerializer(many=True, read_only=True)
    attachments_count = serializers.SerializerMethodField()
    notes_html = serializers.SerializerMethodField()
    total_amount = serializers.ReadOnlyField()
    cash_impact = serializers.ReadOnlyField()
    frozen_cash = serializers.ReadOnlyField()
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Trade
        fields = [
            'id', 'account', 'account_info', 'security', 'security_info', 
            'action', 'action_display', 'status', 'status_display',
            'quantity', 'price', 'fee', 'traded_at', 'filled_at',
            'notes', 'notes_html', 'total_amount', 'cash_impact', 'frozen_cash',
            'created_at', 'updated_at', 'attachments', 'attachments_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_attachments_count(self, obj):
        return obj.attachments.count()
    
    def get_notes_html(self, obj):
        """将 Markdown 转换为 HTML"""
        if obj.notes:
            return markdown.markdown(obj.notes, extensions=['extra', 'codehilite'])
        return ''
    
    def get_account_info(self, obj):
        """获取账户信息"""
        if obj.account:
            return {
                'id': obj.account.id,
                'name': obj.account.name,
                'mode': obj.account.mode,
                'mode_display': obj.account.get_mode_display(),
                'market_type': obj.account.market_type,
                'market_type_display': obj.account.get_market_type_display(),
                'currency': obj.account.currency
            }
        return None


class AuditLogSerializer(serializers.ModelSerializer):
    """审计日志序列化器"""
    user = UserSerializer(read_only=True)
    changes_dict = serializers.SerializerMethodField()
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'action', 'model_type', 'model_id',
            'user', 'changes', 'changes_dict', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_changes_dict(self, obj):
        return obj.get_changes_dict()


class MarketAccountSerializer(serializers.ModelSerializer):
    """市场账户序列化器"""
    mode_display = serializers.CharField(source='get_mode_display', read_only=True)
    market_type_display = serializers.CharField(source='get_market_type_display', read_only=True)
    currency_display = serializers.CharField(source='get_currency_display', read_only=True)
    current_cash = serializers.SerializerMethodField()
    trade_count = serializers.SerializerMethodField()
    
    class Meta:
        model = MarketAccount
        fields = [
            'id', 'owner', 'mode', 'mode_display', 'market_type', 'market_type_display',
            'name', 'currency', 'currency_display', 'start_cash', 'current_cash', 'trade_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']
    
    def get_current_cash(self, obj):
        """计算当前现金"""
        from decimal import Decimal
        
        # 起始资金
        current_cash = obj.start_cash
        
        # 加上所有资金调整
        adjustments_sum = obj.adjustments.aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0')
        current_cash += adjustments_sum
        
        # 减去已成交交易的现金影响
        filled_trades = obj.trades.filter(status='FILLED')
        for trade in filled_trades:
            # 开多/平空：-金额-手续费
            if trade.action in ['OPEN_LONG', 'CLOSE_SHORT']:
                amount = trade.quantity * trade.price
                current_cash -= (amount + trade.fee)
            # 平多/开空：+金额-手续费
            elif trade.action in ['CLOSE_LONG', 'OPEN_SHORT']:
                amount = trade.quantity * trade.price
                current_cash += (amount - trade.fee)
        
        return float(current_cash)
    
    def get_trade_count(self, obj):
        """获取交易数量"""
        return obj.trades.filter(status='FILLED').count()


class CashAdjustmentSerializer(serializers.ModelSerializer):
    """资金调整序列化器"""
    account_name = serializers.CharField(source='account.name', read_only=True)
    
    class Meta:
        model = CashAdjustment
        fields = [
            'id', 'account', 'account_name', 'date', 'amount', 'reason',
            'attachment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
