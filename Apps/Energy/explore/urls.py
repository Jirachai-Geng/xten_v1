from django.contrib import admin
from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path(r'^api/v1/explore/?$', views.ExploreData.as_view()),
    re_path(r'^api/v1/search_public_sensorTreeDiagram', views.SearchPublicSensorTreeDiagram.as_view()),
    re_path(r'^api/v1/search_public_parameterMdb', views.SearchPublicParameterMdb.as_view()),
    re_path(r'^api/v1/search_public_parameterMeter', views.SearchPublicParameterMeter.as_view()),
]
