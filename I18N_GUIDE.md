# Stocks Lab 国际化实现指南

## 已完成功能

### 1. 基础架构
- ✅ 创建了 `/static/js/i18n.js` 国际化JavaScript库
- ✅ 支持中文（zh-hans）和英文（en）两种语言
- ✅ 使用localStorage保存用户语言偏好

### 2. 登录页面
- ✅ 添加了右上角语言切换器（中文/English）
- ✅ 所有文本内容支持中英文切换
- ✅ 切换语言后自动刷新页面应用新语言

## 使用方法

### 在HTML页面中使用

1. 在页面头部引入i18n.js：
```html
<script src="/static/js/i18n.js"></script>
```

2. 使用翻译函数t()：
```javascript
document.getElementById('element').textContent = t('translation_key');
```

3. 添加语言切换按钮：
```html
<button onclick="setLanguage('zh-hans')">中文</button>
<button onclick="setLanguage('en')">English</button>
```

### 可用的翻译键值

#### 登录相关
- `login_title`: 股票实验室 / Stocks Lab
- `username`: 用户名 / Username
- `password`: 密码 / Password
- `login_button`: 登录 / Login

#### 账户相关
- `market_accounts`: 市场账户 / Market Accounts
- `account_type`: 账户类型 / Account Type
- `market_type`: 市场类型 / Market Type
- `start_cash`: 起始资金 / Initial Capital
- `current_balance`: 当前余额 / Current Balance
- `enter_account`: 进入账户 / Enter Account

#### 交易相关
- `open_long`: 开多 / Buy/Long
- `close_long`: 平多 / Sell/Close Long
- `open_short`: 开空 / Short
- `close_short`: 平空 / Cover/Close Short
- `pending_orders`: 待成交订单 / Pending Orders
- `current_positions`: 当前持仓 / Current Positions
- `trade_records`: 交易记录 / Trade Records

#### 详细字段
- `symbol`: 代码 / Symbol
- `quantity`: 数量 / Quantity
- `price`: 价格 / Price
- `amount`: 金额 / Amount
- `fee`: 手续费 / Fee
- `cash_impact`: 现金影响 / Cash Impact
- `frozen_cash`: 冻结资金 / Frozen Cash

#### 按钮和操作
- `confirm_fill`: 确认成交 / Confirm Fill
- `cancel`: 取消 / Cancel
- `close_position`: 平仓 / Close Position
- `add`: 添加 / Add
- `edit`: 编辑 / Edit
- `delete`: 删除 / Delete
- `save`: 保存 / Save

#### 消息提示
- `loading`: 加载中... / Loading...
- `success`: 操作成功 / Success
- `error`: 操作失败 / Error
- `no_data`: 暂无数据 / No Data

## 后续工作清单

### 需要翻译的页面
- [ ] 账户列表页面 (accounts_list.html)
- [ ] 账户详情页面 (account_detail.html)
- [ ] 交易表单页面
- [ ] 导航菜单
- [ ] 各种提示信息

### 实现步骤

1. **在页面头部添加i18n.js**
```html
<script src="/static/js/i18n.js"></script>
```

2. **为需要翻译的元素添加ID**
```html
<h1 id="page-title">市场账户</h1>
<button id="btn-add">添加账户</button>
```

3. **在页面加载时应用翻译**
```javascript
document.addEventListener('DOMContentLoaded', function() {
    applyTranslations();
});

function applyTranslations() {
    document.getElementById('page-title').textContent = t('market_accounts');
    document.getElementById('btn-add').textContent = t('add');
    // ... 更多翻译
}
```

4. **动态内容使用t()函数**
```javascript
const html = `
    <div class="title">${t('symbol')}: ${symbol}</div>
    <div class="price">${t('price')}: ${price}</div>
`;
```

## API翻译

对于Django模型的display字段（如action_display），可以在前端根据语言选择：

```javascript
const actionTexts = {
    'zh-hans': {
        'OPEN_LONG': '开多',
        'CLOSE_LONG': '平多',
        'OPEN_SHORT': '开空',
        'CLOSE_SHORT': '平空'
    },
    'en': {
        'OPEN_LONG': 'Buy/Long',
        'CLOSE_LONG': 'Sell/Close Long',
        'OPEN_SHORT': 'Short',
        'CLOSE_SHORT': 'Cover/Close Short'
    }
};

function getActionText(action) {
    return actionTexts[getCurrentLanguage()][action];
}
```

## 语言持久化

- 语言选择保存在 `localStorage` 中
- 键名: `language`
- 可选值: `zh-hans` (中文) 或 `en` (英文)
- 默认: `zh-hans`

## 测试

1. 访问登录页面
2. 点击右上角的语言切换按钮
3. 验证所有文本是否正确翻译
4. 刷新页面，验证语言偏好是否保持

## 注意事项

1. 所有翻译文本统一在 `/static/js/i18n.js` 中维护
2. 添加新翻译时，需要在两种语言中都添加对应键值
3. 使用语义化的键名，如 `open_long` 而不是 `text1`
4. 对于长文本，可以在翻译文件中使用换行符 `\n`
5. 切换语言后页面会自动刷新以应用新的翻译
