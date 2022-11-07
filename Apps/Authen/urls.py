from django.contrib import admin
from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path(r'^api/v1/authenticate', views.Authenticate.as_view()),
    re_path(r'^api/v1/test_login', views.AuthenticateTEST.as_view()),
    re_path(r'^api/v1/register', views.Register.as_view()),
    re_path(r'^api/v1/canRegis/?$', views.CanRegister.as_view()),
    re_path(r'^api/v1/verify_token', views.VerifyToken.as_view())
]
