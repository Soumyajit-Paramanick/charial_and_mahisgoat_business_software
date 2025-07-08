"""
URL configuration for core project.

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
from django.urls import path, include
from accounts import views as user_views
from accounts.views import export_charial_bills, export_charial_daily_expenses, export_charial_trade, export_balance_sheet
from accounts.views import (
    export_mahisgoat_bills, export_mahisgoat_daily_expenses,
    export_mahisgoat_trade, export_mahisgoat_balance_sheet
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', user_views.home, name='home'),
    path('dashboard/', user_views.dashboard, name='dashboard'),
    
    path('charial/', include([
        path('', user_views.charial_main, name='charial_main'),
        path('bill/', user_views.charial_bill, name='charial_bill'),
        path('daily-expenses/', user_views.charial_daily_expenses, name='charial_daily'),
        path('trade/', user_views.charial_trade, name='charial_trade'),
        path('balance-sheet/', user_views.charial_balance_sheet, name='charial_balance'),
    ])),
    
    path('mahisgoat/', include([
        path('', user_views.mahisgoat_main, name='mahisgoat_main'),
        path('bill/', user_views.mahisgoat_bill, name='mahisgoat_bill'),
        path('daily-expenses/', user_views.mahisgoat_daily_expenses, name='mahisgoat_daily'),
        path('trade/', user_views.mahisgoat_trade, name='mahisgoat_trade'),
        path('balance-sheet/', user_views.mahisgoat_balance_sheet, name='mahisgoat_balance'),
    ])),
    path('charial/export-bills/', export_charial_bills, name='export_charial_bills'),
    path('charial/export-daily/', export_charial_daily_expenses, name='export_charial_daily'),
    path('charial/export-trade/', export_charial_trade, name='export_charial_trade'),
    path('charial/export-balance/', export_balance_sheet, name='export_balance_sheet'),
    path('mahisgoat/export-bills/', export_mahisgoat_bills, name='export_mahisgoat_bills'),
    path('mahisgoat/export-daily/', export_mahisgoat_daily_expenses, name='export_mahisgoat_daily'),
    path('mahisgoat/export-trade/', export_mahisgoat_trade, name='export_mahisgoat_trade'),
    path('mahisgoat/export-balance/', export_mahisgoat_balance_sheet, name='export_mahisgoat_balance'),
]
