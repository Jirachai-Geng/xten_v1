from django.contrib import admin
from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path(r'^api/v1/graph/?$', views.Graph.as_view()),
]
