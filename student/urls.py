from django.urls import path,include
from . import views
from django.contrib import admin



urlpatterns = [
    path('confirm_form/', views.confirm_form, name='confirm_form'),
    path('trans_comp/', views.trans_comp, name='trans_comp'),
    path('calendar/', views.calendar_view, name="calendar"),
    path('form/', views.form_view, name="form"),
    path('my_reservations/', views.my_reservations_form, name='my_reservations_form'),
    path('my_reservations/result/', views.my_reservations, name='my_reservations'),
    path('base', views.base, name='base'),
    path('my_reservations/cancel/<int:pk>/',views.my_reservation_cancel,name='my_reservation_cancel'),
]