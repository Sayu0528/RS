# RS/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.toppage, name='home'),  # トップページのURL
    path('calendar', views.calendar_view, name="calendar")
]
