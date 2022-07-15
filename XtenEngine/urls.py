"""XtenEngine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import re_path, include

urlpatterns = [
    re_path(r'^', include('Apps.Energy.power_quality.urls')),
    re_path(r'^', include('Apps.Energy.explore.urls')),
    re_path(r'^', include('Apps.Billing.tenant.urls')),
    re_path(r'^', include('Apps.Billing.leases.urls')),
    re_path(r'^', include('Apps.Billing.invoice.urls')),
    re_path(r'^', include('Apps.Billing.graph.urls')),
    re_path(r'^', include('Apps.Billing.report_tou.urls')),
    re_path(r'^', include('Apps.Authen.urls')),
]
