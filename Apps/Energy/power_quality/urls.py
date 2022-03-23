from django.contrib import admin
from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path(r'^api/v1/power_quality', views.PowerQuality.as_view()),
    re_path(r'^api/v1/all_meter', views.AllMeter.as_view()),
    re_path(r'^api/v1/search_public_sensorMDB', views.SearchPublicSensorMdb.as_view()),
]
