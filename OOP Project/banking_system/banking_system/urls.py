"""
URL configuration for banking_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from banking_site import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('admin_login/', views.admin_login, name="admin_login"),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_accounts/<str:username>', views.admin_accounts, name='admin_accounts'),
    path('admin_transactions/<str:name>/<str:account_num>', views.admin_transactions_view, name='admin_transactions'),
    path('user_accounts/', views.show, name='show'),
    path('account_creation/', views.account_creation, name='account_creation'),
    path('account_detail/<str:account_type>/<str:acnt_num>', views.account_details, name='account_detail'),
    path('account_detail/<str:account_type>/<str:acnt_num>/deposit', views.account_deposit, name='deposit_page'),
    path('account_detail/<str:account_type>/<str:acnt_num>/withdraw', views.account_withdraw, name='withdraw_page'),
    path('take_loan/<str:act_type>/<str:act_num>', views.take_loan, name='take_loan'),
    path('user_home/', views.user_home, name='user_home'),
    path('account_verification/<str:account_number>', views.account_verification, name='account_verification'),
]
