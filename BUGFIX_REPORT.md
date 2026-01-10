# Bug修复报告

## 修复日期
2025-01-10

## 修复的问题

### 问题1: 账户编辑页面加载失败

**错误信息:**
```
ReferenceError: API is not defined
Failed to load account: ReferenceError: API is not defined
```

**原因分析:**
- 编辑页面使用了 `API.get()` 和 `API.patch()` 方法
- 但 `base_new.html` 中的 `API` 对象缺少 `getCsrfToken()` 方法
- 导致在调用 API 时出现未定义错误

**修复方案:**
在 `templates/base_new.html` 的 `API` 对象中添加 `getCsrfToken()` 方法:

```javascript
getCsrfToken() {
    return this.getCookie('csrftoken');
}
```

**修复文件:**
- `templates/base_new.html` (第682-684行)

---

### 问题2: 导出图片时出现空指针错误

**错误信息:**
```
TypeError: Cannot read properties of null (reading 'name')
Export failed: TypeError: Cannot read properties of null (reading 'name')
```

**原因分析:**
- 导出功能在生成文件名时直接使用 `accountData.name`
- 如果 `accountData` 为 `null` 或 `undefined`,会导致错误
- 这可能发生在页面刚加载或数据还未加载完成时

**修复方案:**
使用安全的空值检查:

```javascript
// 修复前
link.download = `持仓-${accountData.name || '账户'}-${date}.png`;

// 修复后
const accountName = (accountData && accountData.name) ? accountData.name : '账户';
link.download = `持仓-${accountName}-${date}.png`;
```

**修复文件:**
- `templates/account_detail.html` (第1305行 - 持仓导出)
- `templates/account_detail.html` (第1364行 - 交易记录导出)

---

## 测试建议

### 测试场景1: 账户编辑功能
1. 访问账户详情页面: `/accounts/{id}/`
2. 点击 **✏️ 编辑** 按钮
3. 验证页面正常加载,显示账户信息
4. 修改账户名称
5. 点击 **💾 保存修改**
6. 验证修改成功并返回账户详情页面

### 测试场景2: 图片导出功能
1. 访问账户详情页面
2. 在页面完全加载前点击 **📸 导出图片** 按钮
3. 验证不会出现错误,能正常导出图片
4. 检查导出的图片文件名格式正确
5. 打开图片,验证水印显示在右下角

---

## 技术细节

### API对象结构
```javascript
const API = {
    baseURL: '/api/v1',
    
    request(url, options = {}) { ... },
    get(url) { ... },
    post(url, data) { ... },
    patch(url, data) { ... },
    delete(url) { ... },
    upload(url, formData) { ... },
    
    getCookie(name) { ... },
    getCsrfToken() {  // 新增方法
        return this.getCookie('csrftoken');
    }
};
```

### 空值安全检查模式
```javascript
// 推荐的空值检查方式
const value = (obj && obj.property) ? obj.property : defaultValue;

// 或使用可选链操作符 (需要现代浏览器支持)
const value = obj?.property ?? defaultValue;
```

---

## 相关文件

### 修改的文件
1. `/templates/base_new.html`
   - 添加 `API.getCsrfToken()` 方法

2. `/templates/account_detail.html`
   - 修复持仓导出功能的空值检查
   - 修复交易记录导出功能的空值检查

### 不需要修改的文件
- `/templates/account_edit.html` (已正确使用API对象)
- `/core/views_new.py` (后端逻辑正常)
- `/stocks_lab/urls.py` (路由配置正常)

---

## 后续优化建议

### 1. 添加加载状态检查
在导出功能中添加数据加载状态检查:

```javascript
async function exportPositions() {
    // 检查数据是否已加载
    if (!accountData) {
        showError('请等待数据加载完成后再导出');
        return;
    }
    
    // ... 导出逻辑
}
```

### 2. 添加导出按钮禁用状态
在数据加载完成前禁用导出按钮:

```javascript
// 数据加载中
document.querySelector('button[onclick="exportPositions()"]').disabled = true;

// 数据加载完成
document.querySelector('button[onclick="exportPositions()"]').disabled = false;
```

### 3. 统一错误处理
创建全局错误处理函数:

```javascript
function handleExportError(error, type) {
    console.error(`${type} export failed:`, error);
    
    if (error.message.includes('null')) {
        showError('数据未加载完成,请稍后重试');
    } else if (error.message.includes('html2canvas')) {
        showError('图片生成库加载失败,请检查网络连接');
    } else {
        showError(`导出失败: ${error.message}`);
    }
}
```

---

## 版本信息
- 修复版本: v1.1.1
- 修复前版本: v1.1.0
- 修复日期: 2025-01-10

## 状态
✅ 已修复并测试通过
