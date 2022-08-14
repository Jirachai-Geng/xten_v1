from django.contrib import admin
from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path(r'^api/v1/authenticate', views.Authenticate.as_view()),
    re_path(r'^api/v1/register', views.Register.as_view()),
    re_path(r'^api/v1/canRegis/?$', views.CanRegister.as_view()),
    re_path(r'^api/v1/gamescore', views.GameScore.as_view()),
    re_path(r'^api/v1/share', views.GameShare.as_view()),
]
