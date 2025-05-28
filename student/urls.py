from django.urls import path,include
from . import views
from django.contrib import admin


urlpatterns = [
        path('calendar/', views.calendar_view, name="calendar"),
        path('form/', views.form_view, name="form"),
]