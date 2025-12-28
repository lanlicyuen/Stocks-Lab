from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectMember, DailyBalance, Trade, MarketAccount


@login_required
def dashboard_view(request):
    """仪表盘页面"""
    # 获取用户的项目
    if request.user.is_superuser:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(members__user=request.user).distinct()
    
    # 如果有项目，选择第一个作为默认项目
    selected_project = None
    latest_balance = None
    recent_trades = []
    
    if projects.exists():
        project_id = request.GET.get('project')
        if project_id:
            selected_project = get_object_or_404(Project, id=project_id)
        else:
            selected_project = projects.first()
        
        # 获取最新结余
        latest_balance = DailyBalance.objects.filter(
            project=selected_project
        ).order_by('-date').first()
        
        # 获取最近5笔交易
        recent_trades = Trade.objects.filter(
            project=selected_project
        ).order_by('-executed_at')[:5]
    
    context = {
        'projects': projects,
        'selected_project': selected_project,
        'latest_balance': latest_balance,
        'recent_trades': recent_trades,
    }
    return render(request, 'dashboard.html', context)


@login_required
def projects_view(request):
    """项目列表页面"""
    if request.user.is_superuser:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(members__user=request.user).distinct()
    
    return render(request, 'projects.html', {'projects': projects})


@login_required
def project_detail_view(request, pk):
    """项目详情页面"""
    project = get_object_or_404(Project, id=pk)
    
    # 检查权限
    if not request.user.is_superuser:
        if not ProjectMember.objects.filter(project=project, user=request.user).exists():
            return render(request, '403.html', status=403)
    
    members = project.members.all()
    latest_balance = DailyBalance.objects.filter(project=project).order_by('-date').first()
    
    context = {
        'project': project,
        'members': members,
        'latest_balance': latest_balance,
    }
    return render(request, 'project_detail.html', context)


@login_required
def balances_view(request, pk):
    """日结余页面"""
    project = get_object_or_404(Project, id=pk)
    
    # 检查权限
    if not request.user.is_superuser:
        if not ProjectMember.objects.filter(project=project, user=request.user).exists():
            return render(request, '403.html', status=403)
    
    balances = DailyBalance.objects.filter(project=project).order_by('-date')
    
    # 获取用户角色
    my_role = None
    if not request.user.is_superuser:
        try:
            member = ProjectMember.objects.get(project=project, user=request.user)
            my_role = member.role
        except ProjectMember.DoesNotExist:
            pass
    else:
        my_role = 'ADMIN'
    
    context = {
        'project': project,
        'balances': balances,
        'my_role': my_role,
    }
    return render(request, 'balances.html', context)


@login_required
def trades_view(request, pk):
    """交易记录页面"""
    project = get_object_or_404(Project, id=pk)
    
    # 检查权限
    if not request.user.is_superuser:
        if not ProjectMember.objects.filter(project=project, user=request.user).exists():
            return render(request, '403.html', status=403)
    
    trades = Trade.objects.filter(project=project).order_by('-executed_at')
    
    # 获取用户角色
    my_role = None
    if not request.user.is_superuser:
        try:
            member = ProjectMember.objects.get(project=project, user=request.user)
            my_role = member.role
        except ProjectMember.DoesNotExist:
            pass
    else:
        my_role = 'ADMIN'
    
    context = {
        'project': project,
        'trades': trades,
        'my_role': my_role,
    }
    return render(request, 'trades.html', context)


@login_required
def contributions_view(request, pk):
    """出资记录页面"""
    project = get_object_or_404(Project, id=pk)
    
    # 检查权限
    if not request.user.is_superuser:
        if not ProjectMember.objects.filter(project=project, user=request.user).exists():
            return render(request, '403.html', status=403)
    
    contributions = project.contributions.all().order_by('-contributed_at')
    
    # 获取用户角色
    my_role = None
    if not request.user.is_superuser:
        try:
            member = ProjectMember.objects.get(project=project, user=request.user)
            my_role = member.role
        except ProjectMember.DoesNotExist:
            pass
    else:
        my_role = 'ADMIN'
    
    context = {
        'project': project,
        'contributions': contributions,
        'my_role': my_role,
    }
    return render(request, 'contributions.html', context)


@login_required
def account_form_view(request):
    """市场账户创建页面"""
    return render(request, 'account_form.html')


@login_required
def account_detail_view(request, pk):
    """市场账户详情页面"""
    account = get_object_or_404(MarketAccount, id=pk)
    
    # 检查权限：只有账户所有者可以访问
    if not request.user.is_superuser and account.owner != request.user:
        return render(request, '403.html', status=403)
    
    context = {
        'account_id': pk,
        'user_role': 'ADMIN' if request.user.is_superuser or account.owner == request.user else 'VIEWER'
    }
    
    return render(request, 'account_detail.html', context)


@login_required
def security_form_view(request, account_id):
    """新增标的表单页面"""
    account = get_object_or_404(MarketAccount, id=account_id)
    
    # 检查权限
    if not request.user.is_superuser and account.owner != request.user:
        return render(request, '403.html', status=403)
    
    context = {
        'account_id': account_id
    }
    
    return render(request, 'security_form.html', context)


@login_required
def trade_form_view(request, account_id):
    """新增交易表单页面"""
    account = get_object_or_404(MarketAccount, id=account_id)
    
    # 检查权限
    if not request.user.is_superuser and account.owner != request.user:
        return render(request, '403.html', status=403)
    
    context = {
        'account_id': account_id
    }
    
    return render(request, 'trade_form.html', context)

