from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shift_schedule/', views.shift_schedule, name='shift_schedule'),
    path('job_explain/', views.job_explain, name='job_explain'),
]
