# RS/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.toppage, name='home'),  # トップページのURL
]
