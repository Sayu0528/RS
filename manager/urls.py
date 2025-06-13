from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [
    path('top/', views.index, name='index'),
    path('shift_schedule/', views.shift_schedule, name='shift_schedule'),
    path('job_explain/', views.job_explain, name='job_explain'),
    path('calendar-admin/', views.calendar_admin_view, name='admin_calendar'),
    path('manager/<date>/', views.input_by_date_admin_view, name='admin_input_by_date'),
]
