from django.urls import path,include
from . import views
from django.contrib import admin

app_name = "student"

urlpatterns = [
    path('confirm_form/', views.confirm_form, name='confirm_form'),
    path('trans_comp/', views.trans_comp, name='trans_comp'),
    path('calendar/', views.calendar_view, name="calendar"),
    path('form/', views.form_view, name="form"),
    path('my_reservations/', views.my_reservations_form, name='my_reservations_form'),
    path('my_reservations/result/', views.my_reservations, name='my_reservations'),
]