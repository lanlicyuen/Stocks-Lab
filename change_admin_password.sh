#!/bin/bash

# 修改管理员密码脚本
# 使用方法: ./change_admin_password.sh

echo "=== 修改Django管理员密码 ==="

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "错误: 未找到虚拟环境目录 'venv'"
    exit 1
fi

# 获取新密码
echo -n "请输入新密码: "
read -s NEW_PASSWORD
echo

# 验证密码不为空
if [ -z "$NEW_PASSWORD" ]; then
    echo "❌ 错误: 密码不能为空"
    exit 1
fi

# 确认密码
echo -n "请再次输入新密码: "
read -s CONFIRM_PASSWORD
echo

# 验证两次密码是否一致
if [ "$NEW_PASSWORD" != "$CONFIRM_PASSWORD" ]; then
    echo "❌ 错误: 两次输入的密码不一致"
    exit 1
fi

echo "正在修改admin用户的密码..."

# 使用Django shell修改密码
python manage.py shell -c "
from django.contrib.auth.models import User
try:
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('$NEW_PASSWORD')
    admin_user.save()
    print('✅ 管理员密码修改成功!')
    print('用户名: admin')
    print('登录地址: http://localhost:20002/admin/')
except User.DoesNotExist:
    print('❌ 错误: 未找到admin用户')
    print('请先创建管理员账户: ./manage.sh admin')
except Exception as e:
    print(f'❌ 修改密码时出错: {e}')
"

echo "=== 完成 ==="
