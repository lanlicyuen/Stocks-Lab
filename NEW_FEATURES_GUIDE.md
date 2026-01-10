# 新功能使用指南

本文档介绍了 Stocks-Lab 项目新增的功能。

## 功能1: 导出持仓和交易记录图片

### 功能说明
在账户详情页面,你可以将当前持仓和交易记录导出为图片,方便分享和保存。

### 使用方法
1. 进入账户详情页面: `/accounts/{账户ID}/`
2. 在"当前持仓"卡片右上角,点击 **📸 导出图片** 按钮
3. 在"交易记录"卡片右上角,点击 **📸 导出图片** 按钮
4. 图片会自动下载到你的下载文件夹

### 图片规格
- **持仓图片**: 1200x800px (3:2 比例)
- **交易记录图片**: 1200x1600px (3:4 比例)
- **水印位置**: 右下角
- **水印内容**: "Stocks-Lab | 导出时间"
- **水印样式**: 半透明黑色文字 (opacity: 0.4)

### 技术实现
- 使用 `html2canvas` 库将 HTML 元素转换为图片
- 自动添加水印标识
- 文件名格式: `持仓-账户名-日期.png` 或 `交易记录-账户名-日期.png`

### 示例图片位置建议
如果你想提供示例图片供参考,建议放在以下位置:
```
/home/lanlic/Html-Project/Stocks-Lab/static/images/export-examples/
├── positions-example.png      (持仓示例图片 - 1200x800px)
└── trades-example.png         (交易记录示例图片 - 1200x1600px)
```

---

## 功能2: 账户编辑功能

### 功能说明
现在你可以编辑账户的名称,而不需要删除后重新创建。这样可以避免误操作导致数据丢失。

### 使用方法

#### 方式1: 从账户详情页面编辑
1. 进入账户详情页面: `/accounts/{账户ID}/`
2. 点击右上角的 **✏️ 编辑** 按钮
3. 修改账户名称
4. 点击 **💾 保存修改** 按钮

#### 方式2: 从账户管理页面编辑
1. 进入账户管理页面: `/accounts/manage/`
2. 找到要编辑的账户
3. 点击 **编辑** 按钮
4. 修改账户名称
5. 点击 **💾 保存修改** 按钮

### 可编辑字段
- ✅ **账户名称**: 可以修改
- ❌ **市场类型**: 创建后不可修改
- ❌ **账号模式**: 创建后不可修改
- ❌ **币种**: 创建后不可修改
- ❌ **起始资金**: 创建后不可修改

### 注意事项
- 账户名称不能为空
- 修改后会自动返回账户详情页面
- 所有修改会记录到审计日志中

---

## API 端点

### 更新账户信息
```http
PATCH /api/v1/accounts/{id}/
Content-Type: application/json

{
  "name": "新的账户名称"
}
```

**响应示例:**
```json
{
  "id": 1,
  "name": "新的账户名称",
  "mode": "SIM",
  "mode_display": "模拟账号",
  "market_type": "US_STOCK",
  "market_type_display": "美股",
  "currency": "USD",
  "start_cash": "10000.00",
  "created_at": "2025-01-10T10:00:00Z",
  "updated_at": "2025-01-10T14:30:00Z"
}
```

---

## 页面路由

### 新增路由
- `/accounts/{id}/edit/` - 账户编辑页面

### 现有路由
- `/accounts/` - 账户列表页面
- `/accounts/manage/` - 账户管理页面
- `/accounts/{id}/` - 账户详情页面
- `/accounts/{id}/securities/new/` - 新增股票页面
- `/accounts/{id}/trades/new/` - 新增交易页面

---

## 文件清单

### 新增文件
1. `/templates/account_edit.html` - 账户编辑页面模板

### 修改文件
1. `/templates/account_detail.html` - 添加编辑按钮和导出功能
2. `/templates/accounts_manage.html` - 添加编辑按钮
3. `/core/views_new.py` - 添加账户编辑视图函数
4. `/stocks_lab/urls.py` - 添加账户编辑路由

---

## 常见问题

### Q1: 导出的图片在哪里?
A: 图片会自动下载到浏览器的默认下载文件夹,文件名格式为 `持仓-账户名-日期.png` 或 `交易记录-账户名-日期.png`。

### Q2: 为什么有些字段不能编辑?
A: 市场类型、账号模式、币种和起始资金这些字段在创建账户时确定,之后不能修改,以保证数据的一致性和完整性。

### Q3: 导出图片失败怎么办?
A: 请确保:
- 浏览器支持 HTML5 Canvas API
- 网络连接正常(需要加载 html2canvas 库)
- 页面数据已完全加载

### Q4: 编辑账户名称后会影响历史数据吗?
A: 不会。编辑账户名称只是修改显示名称,不会影响任何历史交易记录、持仓数据或统计信息。

---

## 技术细节

### 图片导出实现
```javascript
// 使用 html2canvas 库
await html2canvas(element, {
    backgroundColor: '#ffffff',
    scale: 2,              // 高清输出
    logging: false,
    width: 1200,           // 固定宽度
    height: 800/1600       // 根据内容类型设置高度
});

// 添加水印
ctx.font = '16px Arial';
ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
ctx.textAlign = 'right';
ctx.fillText(watermarkText, canvas.width - 20, canvas.height - 20);
```

### 账户编辑实现
- 前端使用 `API.patch()` 方法调用后端 API
- 后端使用 Django REST Framework 的 `perform_update` 方法
- 自动记录审计日志

---

## 更新日期
2025-01-10

## 版本
v1.1.0
