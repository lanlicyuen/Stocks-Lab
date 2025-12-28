from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import json


class MarketAccount(models.Model):
    """市场账户 - 一级实体，支持模拟/真实模式"""
    MODE_CHOICES = [
        ('SIM', '模拟账号'),
        ('REAL', '真实账号'),
    ]
    
    MARKET_TYPE_CHOICES = [
        ('US_STOCK', '美股'),
        ('CN_A', 'A股'),
        ('HK_STOCK', '港股'),
        ('CRYPTO', '加密货币'),
    ]
    
    CURRENCY_CHOICES = [
        ('USD', '美元'),
        ('CNY', '人民币'),
        ('HKD', '港币'),
        ('USDT', 'USDT'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='market_accounts', verbose_name='所有者')
    mode = models.CharField('账号模式', max_length=10, choices=MODE_CHOICES, default='SIM')
    market_type = models.CharField('市场类型', max_length=20, choices=MARKET_TYPE_CHOICES)
    name = models.CharField('账户名称', max_length=100, blank=True)
    currency = models.CharField('币种', max_length=10, choices=CURRENCY_CHOICES)
    start_cash = models.DecimalField('起始资金', max_digits=15, decimal_places=2)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '市场账户'
        verbose_name_plural = '市场账户'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', 'mode']),
            models.Index(fields=['owner', 'market_type']),
        ]
    
    def __str__(self):
        display_name = self.name or self.get_market_type_display()
        return f'{display_name} ({self.get_mode_display()}) - {self.currency} {self.start_cash}'
    
    def save(self, *args, **kwargs):
        # 自动设置默认名称为市场类型中文
        if not self.name:
            self.name = self.get_market_type_display()
        
        # 自动设置默认币种
        if not self.currency:
            currency_map = {
                'US_STOCK': 'USD',
                'CN_A': 'CNY',
                'HK_STOCK': 'HKD',
                'CRYPTO': 'USDT',
            }
            self.currency = currency_map.get(self.market_type, 'USD')
        super().save(*args, **kwargs)


class Security(models.Model):
    """标的主档 (Security Master)"""
    ASSET_TYPE_CHOICES = [
        ('STOCK', '股票'),
        ('ETF', 'ETF'),
        ('CRYPTO', '加密货币'),
    ]
    
    account = models.ForeignKey(MarketAccount, on_delete=models.CASCADE, related_name='securities', verbose_name='账户')
    symbol = models.CharField('标的代码', max_length=20)
    name = models.CharField('名称', max_length=200)
    asset_type = models.CharField('资产类型', max_length=20, choices=ASSET_TYPE_CHOICES)
    sector = models.CharField('行业分类', max_length=100, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '标的主档'
        verbose_name_plural = '标的主档'
        unique_together = ['account', 'symbol']
        ordering = ['symbol']
        indexes = [
            models.Index(fields=['account', 'asset_type']),
            models.Index(fields=['account', 'symbol']),
        ]
    
    def __str__(self):
        return f'{self.symbol} - {self.name}'
    
    def save(self, *args, **kwargs):
        # 自动转换 symbol 为大写
        self.symbol = self.symbol.upper()
        super().save(*args, **kwargs)


class CashAdjustment(models.Model):
    """资金调整记录 - 用于记录手续费、利息、滑点等非交易类资金变动"""
    account = models.ForeignKey(MarketAccount, on_delete=models.CASCADE, related_name='adjustments', verbose_name='账户')
    date = models.DateField('调整日期')
    amount = models.DecimalField('调整金额', max_digits=15, decimal_places=2, help_text='正数为入金，负数为出金')
    reason = models.TextField('调整原因')
    attachment = models.FileField('附件', upload_to='adjustments/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '资金调整'
        verbose_name_plural = '资金调整'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['account', 'date']),
        ]
    
    def __str__(self):
        sign = '+' if self.amount >= 0 else ''
        return f'{self.account.name} - {self.date} - {sign}{self.amount}'
        return f'{self.account.name} - {self.date} - {sign}{self.amount}'


class Trade(models.Model):
    """交易记录 - 支持做多/做空"""
    ACTION_CHOICES = [
        ('OPEN_LONG', '开多'),
        ('CLOSE_LONG', '平多'),
        ('OPEN_SHORT', '开空'),
        ('CLOSE_SHORT', '平空'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', '待成交'),
        ('FILLED', '已成交'),
        ('CANCELLED', '已取消'),
    ]
    
    account = models.ForeignKey(MarketAccount, on_delete=models.CASCADE, related_name='trades', verbose_name='账户')
    security = models.ForeignKey(Security, on_delete=models.CASCADE, related_name='trades', verbose_name='标的')
    action = models.CharField('交易动作', max_length=20, choices=ACTION_CHOICES)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='PENDING')
    quantity = models.DecimalField('数量', max_digits=15, decimal_places=4)
    price = models.DecimalField('价格', max_digits=15, decimal_places=4)
    fee = models.DecimalField('手续费', max_digits=15, decimal_places=2, default=0)
    traded_at = models.DateTimeField('交易时间', null=True, blank=True, help_text='实际交易时间，PENDING订单可为空')
    filled_at = models.DateTimeField('成交时间', null=True, blank=True, help_text='订单成交的时间')
    notes = models.TextField('备注', blank=True, help_text='支持 Markdown 格式')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '交易记录'
        verbose_name_plural = '交易记录'
        ordering = ['-traded_at', '-id']
        indexes = [
            models.Index(fields=['account', '-traded_at']),
            models.Index(fields=['account', 'security']),
            models.Index(fields=['account', 'status']),
        ]
    
    def __str__(self):
        return f'{self.security.symbol} - {self.get_action_display()} - {self.quantity}@{self.price}'
    
    @property
    def total_amount(self):
        """交易总金额（不含手续费）"""
        return float(self.quantity) * float(self.price)
    
    @property
    def cash_impact(self):
        """对现金的影响（负数表示支出）
        注意: 只有FILLED状态的交易才真正影响现金
        """
        # 如果订单未成交，不影响现金（但会冻结资金）
        if self.status != 'FILLED':
            return 0
            
        amount = self.total_amount
        fee = float(self.fee)
        
        if self.action == 'OPEN_LONG':
            # 开多: 支付金额 + 手续费
            return -(amount + fee)
        elif self.action == 'CLOSE_LONG':
            # 平多: 收到金额 - 手续费
            return amount - fee
        elif self.action == 'OPEN_SHORT':
            # 开空: 收到金额 - 手续费
            return amount - fee
        elif self.action == 'CLOSE_SHORT':
            # 平空: 支付金额 + 手续费
            return -(amount + fee)
    
    @property
    def frozen_cash(self):
        """冻结资金（PENDING状态时冻结的金额）"""
        if self.status != 'PENDING':
            return 0
            
        amount = self.total_amount
        fee = float(self.fee)
        
        # 只有开多和平空需要冻结资金
        if self.action in ['OPEN_LONG', 'CLOSE_SHORT']:
            return amount + fee
        return 0


class TradeAttachment(models.Model):
    """交易附件（截图、PDF等）"""
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='attachments', verbose_name='交易')
    file = models.FileField('文件', upload_to='trade_attachments/%Y/%m/%d/')
    file_type = models.CharField('文件类型', max_length=50, blank=True)  # image/png, application/pdf
    file_size = models.IntegerField('文件大小(字节)', default=0)
    description = models.CharField('描述', max_length=200, blank=True)
    uploaded_at = models.DateTimeField('上传时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '交易附件'
        verbose_name_plural = '交易附件'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f'{self.trade.symbol} - {self.file.name}'
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            import mimetypes
            self.file_type = mimetypes.guess_type(self.file.name)[0] or 'application/octet-stream'
        super().save(*args, **kwargs)


class AuditLog(models.Model):
    """审计日志"""
    ACTION_CHOICES = [
        ('CREATE', '创建'),
        ('UPDATE', '更新'),
        ('DELETE', '删除'),
    ]
    
    action = models.CharField('操作', max_length=10, choices=ACTION_CHOICES)
    model_type = models.CharField('模型类型', max_length=50)
    model_id = models.IntegerField('模型ID')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs', verbose_name='操作人')
    changes = models.TextField('变更内容', blank=True)  # JSON format
    created_at = models.DateTimeField('操作时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '审计日志'
        verbose_name_plural = '审计日志'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['model_type', 'model_id']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f'{self.get_action_display()} - {self.model_type} #{self.model_id} by {self.user}'
    
    def get_changes_dict(self):
        """获取变更内容字典"""
        try:
            return json.loads(self.changes) if self.changes else {}
        except json.JSONDecodeError:
            return {}
