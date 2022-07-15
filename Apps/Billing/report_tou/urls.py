from django.contrib import admin
from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path(r'^api/v1/report-tou/?$', views.Report_TOU.as_view()),
]
