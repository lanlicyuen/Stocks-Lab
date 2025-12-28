// Internationalization for Stocks Lab
const translations = {
    'zh-hans': {
        // Site
        'site_title': '投资披露平台',
        'account_settings': '账号管理',
        'logout_menu': '登出',
        
        // Login page
        'login_title': '股票实验室',
        'login_subtitle': '模拟交易 · 数据分析',
        'username': '用户名',
        'password': '密码',
        'login_button': '登录',
        'logout': '退出登录',
        'language': '语言',
        
        // Navigation
        'dashboard': '仪表板',
        'home': '首页',
        'accounts': '账户',
        'account_list': '账户列表',
        'account_detail': '账户详情',
        'trades': '交易',
        'portfolio': '投资组合',
        'settings': '设置',
        
        // Account page
        'market_accounts': '市场账户',
        'account_type': '账户类型',
        'simulation': '模拟账号',
        'real': '实盘账号',
        'market_type': '市场类型',
        'us_stock': '美股',
        'hk_stock': '港股',
        'crypto': '加密货币',
        'currency': '币种',
        'start_cash': '起始资金',
        'current_balance': '当前余额',
        'enter_account': '进入账户',
        'trade_count': '交易',
        'trades_count': '笔',
        
        // Account detail
        'pending_orders': '待成交订单',
        'current_positions': '当前持仓',
        'trade_records': '交易记录',
        'operation_records': '操作记录',
        'account_info': '账户信息',
        'created_at': '创建时间',
        'current_cash': '当前现金',
        'total_pnl': '总盈亏',
        'return_pct': '收益率',
        'realized_pnl': '已实现盈亏',
        'trade_statistics': '交易统计',
        'buy_count': '买入笔数',
        'sell_count': '卖出笔数',
        'total_fee': '手续费',
        'add_security': '新增股票',
        'add_trade': '新增交易',
        'cash_adjustment': '资金调整',
        'delete_account': '删除账户',
        'view_all': '展开全部',
        'view_operations': '查看操作记录',
        'click_to_view': '点击下方按钮查看操作记录',
        
        // Form pages
        'add_security_title': '新增交易股票',
        'add_trade_title': '新增交易记录',
        'symbol_label': '标的代码',
        'symbol_placeholder': '例如: AAPL, BTC, 600519',
        'symbol_hint': '代码将自动转为大写',
        'security_name': '股票名称',
        'security_name_placeholder': '例如: 苹果公司, 比特币, 贵州茅台',
        'asset_type_label': '资产类型',
        'asset_type_stock': '股票',
        'asset_type_etf': 'ETF',
        'asset_type_crypto': '加密货币',
        'sector_label': '行业分类',
        'sector_placeholder': '例如: 科技, 消费, 金融',
        'create_security': '创建股票',
        'processing': '处理中...',
        'select_security': '选择标的',
        'no_security_add': '没有找到标的？',
        'click_to_add': '点击新增',
        'action_label': '交易动作',
        'select_placeholder': '请选择...',
        'quantity_label': '数量',
        'quantity_placeholder': '例如: 100',
        'price_label': '价格',
        'price_placeholder': '例如: 150.50',
        'fee_label': '手续费',
        'fee_placeholder': '默认 0',
        'trade_time_label': '交易时间',
        'trade_reason': '交易理由（支持 Markdown）',
        'reason_placeholder': '记录交易逻辑、市场分析、操作依据等...',
        'markdown_hint': '支持 Markdown 语法，可以添加链接、列表等',
        'trade_preview': '交易预览',
        'submit_trade': '提交交易',
        'available_cash': '可用资金',
        'position_value': '持仓价值',
        
        // Cash adjustment modal
        'cash_adjustment_title': '新增资金调整',
        'adjustment_date': '调整日期',
        'adjustment_amount': '调整金额',
        'adjustment_amount_placeholder': '正数为入金，负数为出金',
        'adjustment_amount_hint': '正数表示入金，负数表示出金',
        'adjustment_reason': '调整原因',
        'adjustment_reason_placeholder': '例如：手续费、利息、滑点调整等',
        
        // Delete confirmation
        'confirm_delete_account': '确认删除账户',
        'delete_warning': '此操作将同时删除该账户下的所有股票和交易记录，且无法恢复！',
        'account_deleted': '账户已删除',
        'delete_failed': '删除失败：',
        
        // Trade actions
        'open_long': '开多',
        'open_long_desc': '开多（买入做多）',
        'close_long': '平多',
        'close_long_desc': '平多（卖出平多）',
        'open_short': '开空',
        'open_short_desc': '开空（卖出做空）',
        'close_short': '平空',
        'close_short_desc': '平空（买入平空）',
        'confirm_fill': '确认成交',
        'cancel': '取消',
        'close_position': '平仓',
        
        // Trade details
        'symbol': '代码',
        'quantity': '数量',
        'price': '价格',
        'amount': '金额',
        'fee': '手续费',
        'trade_amount': '交易金额',
        'cash_impact': '现金影响',
        'frozen_cash': '冻结资金',
        'trade_time': '交易时间',
        'filled_time': '成交时间',
        'created_time': '创建时间',
        'notes': '备注',
        
        // Position details
        'position_quantity': '持仓数量',
        'avg_cost': '平均成本',
        'position_value': '持仓金额',
        'long_position': '做多',
        'short_position': '做空',
        
        // Buttons
        'add': '添加',
        'edit': '编辑',
        'delete': '删除',
        'save': '保存',
        'back': '返回',
        'confirm': '确认',
        'view_more': '查看更多',
        
        // Messages
        'loading': '加载中...',
        'no_data': '暂无数据',
        'no_pending_orders': '暂无待成交订单',
        'no_positions': '暂无持仓',
        'no_trades': '暂无交易记录',
        'no_operations': '暂无操作记录',
        'success': '操作成功',
        'error': '操作失败',
        'confirm_fill_msg': '确认成交此订单？\n\n成交后将扣除资金并生成持仓。',
        'confirm_cancel_msg': '确认取消此订单？\n\n取消后将释放冻结资金。',
        'order_filled': '订单已成交！',
        'order_cancelled': '订单已取消',
        'position_closed': '平仓成功！',
    },
    'en': {
        // Site
        'site_title': 'Investment Disclosure Platform',
        'account_settings': 'Account Settings',
        'logout_menu': 'Logout',
        
        // Login page
        'login_title': 'Stocks Lab',
        'login_subtitle': 'Simulation Trading · Data Analysis',
        'username': 'Username',
        'password': 'Password',
        'login_button': 'Login',
        'logout': 'Logout',
        'language': 'Language',
        
        // Navigation
        'dashboard': 'Dashboard',
        'home': 'Home',
        'accounts': 'Accounts',
        'account_list': 'Account List',
        'account_detail': 'Account Detail',
        'trades': 'Trades',
        'portfolio': 'Portfolio',
        'settings': 'Settings',
        
        // Account page
        'market_accounts': 'Market Accounts',
        'account_type': 'Account Type',
        'simulation': 'Simulation',
        'real': 'Real Trading',
        'market_type': 'Market Type',
        'us_stock': 'US Stocks',
        'hk_stock': 'HK Stocks',
        'crypto': 'Cryptocurrency',
        'currency': 'Currency',
        'start_cash': 'Initial Capital',
        'current_balance': 'Current Balance',
        'enter_account': 'Enter Account',
        'trade_count': 'Trade',
        'trades_count': '',
        
        // Account detail
        'pending_orders': 'Pending Orders',
        'current_positions': 'Current Positions',
        'trade_records': 'Trade Records',
        'operation_records': 'Operation Records',
        'account_info': 'Account Info',
        'created_at': 'Created',
        'current_cash': 'Current Cash',
        'total_pnl': 'Total P&L',
        'return_pct': 'Return',
        'realized_pnl': 'Realized P&L',
        'trade_statistics': 'Trade Statistics',
        'buy_count': 'Buys',
        'sell_count': 'Sells',
        'total_fee': 'Total Fee',
        'add_security': 'Add Security',
        'add_trade': 'Add Trade',
        'cash_adjustment': 'Cash Adjustment',
        'delete_account': 'Delete Account',
        'view_all': 'View All',
        'view_operations': 'View Operations',
        'click_to_view': 'Click button below to view operation records',
        
        // Form pages
        'add_security_title': 'Add Security',
        'add_trade_title': 'Add Trade Record',
        'symbol_label': 'Symbol',
        'symbol_placeholder': 'e.g.: AAPL, BTC, 600519',
        'symbol_hint': 'Symbol will be auto-converted to uppercase',
        'security_name': 'Security Name',
        'security_name_placeholder': 'e.g.: Apple Inc, Bitcoin, Moutai',
        'asset_type_label': 'Asset Type',
        'asset_type_stock': 'Stock',
        'asset_type_etf': 'ETF',
        'asset_type_crypto': 'Cryptocurrency',
        'sector_label': 'Sector',
        'sector_placeholder': 'e.g.: Technology, Consumer, Finance',
        'create_security': 'Create Security',
        'processing': 'Processing...',
        'select_security': 'Select Security',
        'no_security_add': 'Security not found?',
        'click_to_add': 'Click to add',
        'action_label': 'Action',
        'select_placeholder': 'Please select...',
        'quantity_label': 'Quantity',
        'quantity_placeholder': 'e.g.: 100',
        'price_label': 'Price',
        'price_placeholder': 'e.g.: 150.50',
        'fee_label': 'Fee',
        'fee_placeholder': 'Default 0',
        'trade_time_label': 'Trade Time',
        'trade_reason': 'Trade Reason (Markdown supported)',
        'reason_placeholder': 'Record trading logic, market analysis, operation basis, etc...',
        'markdown_hint': 'Markdown syntax supported, you can add links, lists, etc.',
        'trade_preview': 'Trade Preview',
        'submit_trade': 'Submit Trade',
        'available_cash': 'Available Cash',
        'position_value': 'Position Value',
        
        // Cash adjustment modal
        'cash_adjustment_title': 'Cash Adjustment',
        'adjustment_date': 'Adjustment Date',
        'adjustment_amount': 'Adjustment Amount',
        'adjustment_amount_placeholder': 'Positive for deposit, negative for withdrawal',
        'adjustment_amount_hint': 'Positive for deposit, negative for withdrawal',
        'adjustment_reason': 'Reason',
        'adjustment_reason_placeholder': 'e.g.: Fee, Interest, Slippage adjustment, etc.',
        
        // Delete confirmation
        'confirm_delete_account': 'Confirm Delete Account',
        'delete_warning': 'This will also delete all securities and trade records under this account, and cannot be recovered!',
        'account_deleted': 'Account deleted',
        'delete_failed': 'Delete failed: ',
        
        // Trade actions
        'open_long': 'Buy/Long',
        'open_long_desc': 'Open Long (Buy)',
        'close_long': 'Sell/Close Long',
        'close_long_desc': 'Close Long (Sell)',
        'open_short': 'Short',
        'open_short_desc': 'Open Short (Sell)',
        'close_short': 'Cover/Close Short',
        'close_short_desc': 'Close Short (Cover)',
        'confirm_fill': 'Confirm Fill',
        'cancel': 'Cancel',
        'close_position': 'Close Position',
        
        // Trade details
        'symbol': 'Symbol',
        'quantity': 'Quantity',
        'price': 'Price',
        'amount': 'Amount',
        'fee': 'Fee',
        'trade_amount': 'Trade Amount',
        'cash_impact': 'Cash Impact',
        'frozen_cash': 'Frozen Cash',
        'trade_time': 'Trade Time',
        'filled_time': 'Filled Time',
        'created_time': 'Created Time',
        'notes': 'Notes',
        
        // Position details
        'position_quantity': 'Position',
        'avg_cost': 'Avg Cost',
        'position_value': 'Position Value',
        'long_position': 'Long',
        'short_position': 'Short',
        
        // Buttons
        'add': 'Add',
        'edit': 'Edit',
        'delete': 'Delete',
        'save': 'Save',
        'back': 'Back',
        'confirm': 'Confirm',
        'view_more': 'View More',
        
        // Messages
        'loading': 'Loading...',
        'no_data': 'No Data',
        'no_pending_orders': 'No pending orders',
        'no_positions': 'No positions',
        'no_trades': 'No trade records',
        'no_operations': 'No operation records',
        'success': 'Success',
        'error': 'Error',
        'confirm_fill_msg': 'Confirm to fill this order?\n\nFunds will be deducted and position will be created.',
        'confirm_cancel_msg': 'Confirm to cancel this order?\n\nFrozen funds will be released.',
        'order_filled': 'Order filled!',
        'order_cancelled': 'Order cancelled',
        'position_closed': 'Position closed!',
    }
};

// Get current language from localStorage or default to Chinese
let currentLang = localStorage.getItem('language') || 'zh-hans';

// Translation function
function t(key) {
    return translations[currentLang][key] || key;
}

// Set language
function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('language', lang);
    // Reload page to apply translations
    location.reload();
}

// Get current language
function getCurrentLanguage() {
    return currentLang;
}
