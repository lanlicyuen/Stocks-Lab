# Stocks-Lab 数据模型文档

## 📊 模型概览

### 核心实体（7个模型）

1. **Project** - 投资项目
2. **ProjectMember** - 项目成员
3. **Contribution** - 出资记录
4. **DailyBalance** - 每日结余
5. **Trade** - 交易记录
6. **Attachment** - 附件
7. **AuditLog** - 审计日志

---

## 🗂️ 详细字段说明

### 1. Project（投资项目）
```python
class Project(models.Model):
    name = CharField(max_length=200)              # 项目名称
    description = TextField(blank=True)           # 项目描述
    created_by = ForeignKey(User)                 # 创建者
    created_at = DateTimeField(auto_now_add=True) # 创建时间
    updated_at = DateTimeField(auto_now=True)     # 更新时间
```

**关系**:
- `members` → ProjectMember (一对多)
- `contributions` → Contribution (一对多)
- `daily_balances` → DailyBalance (一对多)
- `trades` → Trade (一对多)

---

### 2. ProjectMember（项目成员）
```python
class ProjectMember(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', '管理员'),    # 可增删改查
        ('VIEWER', '观察者'),   # 只读权限
    ]
    
    project = ForeignKey(Project)                 # 所属项目
    user = ForeignKey(User)                       # 成员用户
    role = CharField(max_length=10)               # 角色
    joined_at = DateTimeField(auto_now_add=True)  # 加入时间
```

**约束**:
- `unique_together = ['project', 'user']` - 每个用户在项目中唯一

---

### 3. Contribution（出资记录）
```python
class Contribution(models.Model):
    project = ForeignKey(Project)                 # 所属项目
    user = ForeignKey(User)                       # 出资人
    amount = DecimalField(max_digits=15, decimal_places=2)  # 出资金额
    notes = TextField(blank=True)                 # 备注
    contributed_at = DateField()                  # 出资日期
    created_at = DateTimeField(auto_now_add=True) # 记录创建时间
    created_by = ForeignKey(User)                 # 记录人
```

---

### 4. DailyBalance（每日结余）
```python
class DailyBalance(models.Model):
    project = ForeignKey(Project)                 # 所属项目
    date = DateField()                            # 日期
    balance = DecimalField(max_digits=15, decimal_places=2)  # 账户余额
    notes = TextField(blank=True)                 # 备注
    created_by = ForeignKey(User)                 # 记录人
    created_at = DateTimeField(auto_now_add=True) # 创建时间
    updated_at = DateTimeField(auto_now=True)     # 更新时间
```

**约束**:
- `unique_together = ['project', 'date']` - 每个项目每天只有一条记录

**关系**:
- 可通过 `Attachment` 关联多张截图

---

### 5. Trade（交易记录）
```python
class Trade(models.Model):
    SIDE_CHOICES = [
        ('BUY', '买入'),
        ('SELL', '卖出'),
    ]
    
    project = ForeignKey(Project)                 # 所属项目
    symbol = CharField(max_length=20)             # 股票代码
    side = CharField(max_length=4)                # 交易方向
    quantity = IntegerField()                     # 数量
    price = DecimalField(max_digits=15, decimal_places=4)  # 价格
    executed_at = DateTimeField()                 # 执行时间
    thesis = TextField()                          # 交易理论依据（Markdown，必填）
    review = TextField(blank=True)                # 复盘（可选）
    created_by = ForeignKey(User)                 # 记录人
    created_at = DateTimeField(auto_now_add=True) # 创建时间
    updated_at = DateTimeField(auto_now=True)     # 更新时间
```

**计算属性**:
```python
@property
def total_amount(self):
    return float(self.quantity) * float(self.price)
```

**关系**:
- 可通过 `Attachment` 关联多张交易截图

---

### 6. Attachment（附件）
```python
class Attachment(models.Model):
    OWNER_TYPE_CHOICES = [
        ('TRADE', '交易'),
        ('BALANCE', '日结余'),
    ]
    
    owner_type = CharField(max_length=10)         # 所属类型
    owner_id = IntegerField()                     # 所属对象ID
    file = FileField(upload_to='attachments/%Y/%m/%d/')  # 文件
    uploaded_by = ForeignKey(User)                # 上传者
    uploaded_at = DateTimeField(auto_now_add=True)  # 上传时间
```

**索引**:
- `Index(fields=['owner_type', 'owner_id'])` - 查询优化

**方法**:
```python
def get_owner(self):
    """获取所属对象（Trade 或 DailyBalance）"""
```

---

### 7. AuditLog（审计日志）
```python
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', '创建'),
        ('UPDATE', '更新'),
        ('DELETE', '删除'),
    ]
    
    action = CharField(max_length=10)             # 操作类型
    model_type = CharField(max_length=50)         # 模型类型
    model_id = IntegerField()                     # 模型ID
    user = ForeignKey(User, null=True)            # 操作人
    changes = TextField(blank=True)               # 变更内容（JSON）
    created_at = DateTimeField(auto_now_add=True) # 操作时间
```

**索引**:
- `Index(fields=['model_type', 'model_id'])` - 按对象查询
- `Index(fields=['created_at'])` - 按时间查询

**方法**:
```python
def get_changes_dict(self):
    """解析 JSON 格式的变更内容"""
    return json.loads(self.changes) if self.changes else {}
```

---

## 🔗 实体关系图

```
User ──┬──> Project (created_by)
       ├──> ProjectMember (user)
       ├──> Contribution (user, created_by)
       ├──> DailyBalance (created_by)
       ├──> Trade (created_by)
       ├──> Attachment (uploaded_by)
       └──> AuditLog (user)

Project ──┬──> ProjectMember (project)
          ├──> Contribution (project)
          ├──> DailyBalance (project)
          └──> Trade (project)

Trade ──┐
        ├──> Attachment (owner_type='TRADE', owner_id)
DailyBalance ──┘
```

---

## 🔐 权限设计

### ProjectMember.role

| 角色 | 权限 |
|------|------|
| **ADMIN** | 可以增删改查所有数据 |
| **VIEWER** | 只能查看，不能修改 |

---

## 📝 特殊约束

### 唯一性约束
1. **ProjectMember**: `(project, user)` - 用户在项目中唯一
2. **DailyBalance**: `(project, date)` - 每个项目每天只有一条结余记录

### 必填字段
- **Trade.thesis** - 交易理论依据（Markdown 格式）必填
- 所有金额字段使用 `DecimalField` 保证精度

### 级联删除
- `Project` 删除 → 级联删除 `ProjectMember`, `Contribution`, `DailyBalance`, `Trade`
- `User` 删除 → 使用 `PROTECT` 防止误删（需先解除关联）

---

## 🛠️ Django Admin 配置

所有模型已在 `core/admin.py` 中注册：

```python
@admin.register(Project)
@admin.register(ProjectMember)
@admin.register(Contribution)
@admin.register(DailyBalance)
@admin.register(Trade)
@admin.register(Attachment)
@admin.register(AuditLog)
```

**Admin 功能**:
- ✅ 列表展示（list_display）
- ✅ 搜索功能（search_fields）
- ✅ 过滤器（list_filter）
- ✅ 排序（ordering）
- ✅ 只读字段（readonly_fields，仅 AuditLog）

---

## 📊 数据迁移

**生成的迁移文件**:
```
core/migrations/0001_initial.py
```

**执行命令**:
```bash
python manage.py makemigrations core
python manage.py migrate
```

**验证命令**:
```bash
python verify_models.py
```

---

## 🎯 使用示例

### 创建项目和成员
```python
from django.contrib.auth.models import User
from core.models import Project, ProjectMember

# 创建项目
user = User.objects.create_user('admin', password='admin123')
project = Project.objects.create(
    name='投资项目A',
    description='测试项目',
    created_by=user
)

# 添加管理员
ProjectMember.objects.create(
    project=project,
    user=user,
    role='ADMIN'
)
```

### 记录交易和附件
```python
from core.models import Trade, Attachment

# 创建交易
trade = Trade.objects.create(
    project=project,
    symbol='AAPL',
    side='BUY',
    quantity=100,
    price=150.25,
    executed_at=timezone.now(),
    thesis='# 买入理由\n\n技术突破，看涨...',
    created_by=user
)

# 上传交易截图
attachment = Attachment.objects.create(
    owner_type='TRADE',
    owner_id=trade.id,
    file='path/to/screenshot.png',
    uploaded_by=user
)
```

### 查询审计日志
```python
from core.models import AuditLog

# 查看某个交易的所有变更记录
logs = AuditLog.objects.filter(
    model_type='Trade',
    model_id=trade.id
).order_by('-created_at')
```

---

## ✅ 验证清单

- [x] 7个数据模型全部创建
- [x] 所有关系正确配置
- [x] 唯一性约束已设置
- [x] 必填字段已标注
- [x] Django Admin 全部注册
- [x] 数据库迁移已完成
- [x] 模型验证脚本通过

---

**更新时间**: 2025-12-27  
**数据库**: SQLite3  
**Django版本**: 4.2.9  
**DRF版本**: 3.14.0
