# manager/urls.py
from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
    # トップページ（index.html）
    path('',                   views.index,            name='index'),

    # toppage.html（/toppage/）
    path('toppage/',           views.toppage,          name='toppage'),

    # シフト入力（shift_schedule.html）
    path('shift_schedule/',    views.shift_schedule,   name='shift_input'),

    # 出席者名簿（attendance_list.html）
    path('attendance_list/',   views.attendance_list,  name='attendance_list'),

    # 仕事内容入力（job_explain.html）
    path('job_explain/',       views.job_explain,      name='job_entry'),
]
