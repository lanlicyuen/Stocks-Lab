from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views_new

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API
    path('api/v1/', include('core.urls')),
    
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='login_new.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    
    # Main pages (accounts only)
    path('', views_new.accounts_list_view, name='dashboard'),
    path('accounts/', views_new.accounts_list_view, name='accounts_list'),
    path('accounts/manage/', views_new.accounts_manage_view, name='accounts_manage'),
    path('accounts/<int:pk>/', views_new.account_detail_view, name='account_detail'),
    path('accounts/<int:pk>/edit/', views_new.account_edit_view, name='account_edit'),
    path('accounts/<int:account_id>/securities/manage/', views_new.securities_manage_view, name='securities_manage'),
    path('accounts/<int:account_id>/securities/debug/', views_new.debug_securities_view, name='debug_securities'),
    path('accounts/<int:account_id>/share/', views_new.position_share_view, name='position_share'),
    path('accounts/<int:account_id>/trades/share/', views_new.trade_share_view, name='trade_share'),
    path('accounts/<int:account_id>/securities/new/', views_new.security_form_view, name='security_form'),
    path('accounts/<int:account_id>/trades/new/', views_new.trade_form_view, name='trade_form'),
    path('account', views_new.account_settings_view, name='account_settings'),
]
