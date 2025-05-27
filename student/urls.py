from django.urls import path
from . import views

urlpatterns = [
    path('confirm_form/', views.confirm_form, name='confirm_form'),
    path('trans_comp/', views.trans_comp, name='trans_comp'),
]