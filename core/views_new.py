from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MarketAccount


def login_view(request):
    """登录页面"""
    if request.user.is_authenticated:
        return redirect('accounts_list')
    return render(request, 'login_new.html')


@login_required
def accounts_list_view(request):
    """账户列表页面 - 首页"""
    return render(request, 'accounts_list.html')


@login_required
def accounts_manage_view(request):
    """账户管理页面"""
    return render(request, 'accounts_manage.html')


@login_required
def account_detail_view(request, pk):
    """账户详情页面"""
    return render(request, 'account_detail.html', {
        'account_id': pk
    })


@login_required
def account_settings_view(request):
    """账户设置页面"""
    return render(request, 'account_settings.html')


def security_form_view(request, account_id):
    """新增股票表单页面"""
    # 权限检查由前端JavaScript通过API验证
    context = {
        'account_id': account_id
    }
    
    return render(request, 'security_form.html', context)


def trade_form_view(request, account_id):
    """新增交易表单页面"""
    # 权限检查由前端JavaScript通过API验证
    context = {
        'account_id': account_id
    }
    
    return render(request, 'trade_form.html', context)


@login_required
def account_edit_view(request, pk):
    """账户编辑页面"""
    return render(request, 'account_edit.html', {
        'account_id': pk
    })


@login_required
def securities_manage_view(request, account_id):
    """股票管理页面"""
    return render(request, 'securities_manage.html', {
        'account_id': account_id
    })


@login_required
def debug_securities_view(request, account_id):
    """调试股票管理页面"""
    return render(request, 'debug_securities.html', {
        'account_id': account_id
    })


@login_required
def position_share_view(request, account_id):
    """持仓分享页面"""
    return render(request, 'position_share.html', {
        'account_id': account_id
    })


@login_required
def trade_share_view(request, account_id):
    """交易分享页面"""
    return render(request, 'trade_share.html', {
        'account_id': account_id
    })
