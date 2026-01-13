# 管理员密码修改指南

## 方法一：使用脚本（推荐）

```bash
# 交互式修改密码
./change_admin_password.sh
```

脚本会提示：
1. 输入新密码
2. 再次输入新密码确认
3. 验证密码一致性和有效性
4. 自动修改密码

**安全特性**：
- ✅ 密码输入隐藏显示
- ✅ 必须两次输入确认
- ✅ 验证密码一致性
- ✅ 检查密码非空
- ✅ 详细的错误提示

## 方法二：使用Django命令

```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 启动Django shell
python manage.py shell

# 3. 在shell中执行
from django.contrib.auth.models import User
admin = User.objects.get(username='admin')
admin.set_password('你的新密码')
admin.save()
exit()
```

## 方法三：重新创建管理员

```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 创建新的管理员账户
python manage.py createsuperuser

# 按提示输入用户名、邮箱和密码
```

## 登录地址

- **管理后台**: http://localhost:20002/admin/
- **用户名**: admin
- **密码**: 你设置的新密码

## 注意事项

1. 确保后端服务正在运行（端口20004）
2. 如果忘记密码，可以使用方法三重新创建
3. 建议使用强密码保护管理员账户

## 当前状态

✅ admin用户已存在
✅ 密码修改功能正常
✅ 登录测试通过
