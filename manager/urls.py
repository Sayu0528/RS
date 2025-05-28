from django.urls import path,include
from . import views
from django.contrib import admin

urlpatterns = [
    # 管理者用カレンダー一覧
    path('calendar-admin/', views.calendar_admin_view, name='admin_calendar'),
    # 日付クリック後の入力画面（管理者用）
    path('manager/<date>/', views.input_by_date_admin_view, name='admin_input_by_date'),
]