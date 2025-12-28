from django.contrib import admin
from .models import (
    Trade, TradeAttachment, AuditLog, MarketAccount, CashAdjustment, Security
)

@admin.register(MarketAccount)
class MarketAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'mode', 'market_type', 'currency', 'start_cash', 'created_at')
    list_filter = ('mode', 'market_type', 'created_at')
    search_fields = ('name', 'owner__username')
    ordering = ('-created_at',)

@admin.register(Security)
class SecurityAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'account', 'asset_type', 'sector')
    list_filter = ('asset_type',)
    search_fields = ('symbol', 'name', 'account__name')
    ordering = ('symbol',)

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('account', 'security', 'action', 'quantity', 'price', 'traded_at')
    list_filter = ('action', 'traded_at', 'created_at')
    search_fields = ('account__name', 'security__symbol', 'notes')
    ordering = ('-traded_at',)

@admin.register(TradeAttachment)
class TradeAttachmentAdmin(admin.ModelAdmin):
    list_display = ('trade', 'file_type', 'file_size', 'description', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('trade__security__symbol', 'description')
    ordering = ('-uploaded_at',)

@admin.register(CashAdjustment)
class CashAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('account', 'date', 'amount', 'reason', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('account__name', 'reason')
    ordering = ('-date',)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'model_type', 'model_id', 'user', 'created_at')
    list_filter = ('action', 'model_type', 'created_at')
    search_fields = ('model_type', 'user__username')
    ordering = ('-created_at',)
