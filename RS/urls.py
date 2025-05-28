# RS/urls.py
from django.urls import path,include
from . import views
from django.contrib import admin



urlpatterns = [
    path('', views.toppage, name='home'),  # トップページのURL
]
