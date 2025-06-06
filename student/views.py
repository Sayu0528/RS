from django.shortcuts import render
from django.http import HttpResponse
from datetime import date, timedelta
from django.views import View
from .forms import StudentForm

# Create your views here.

# 入力情報確認画面
def confirm_form(request):
    return render(request, 'student/confirm_form.html')

#送信完了画面
def trans_comp(request):
    return render(request, 'student/trans_comp.html')

def calendar_view(request):
    # GETパラメータ week=YYYY-MM-DD があればその週の月曜を start に、
    # なければ今日が属する週の月曜を start に設定
    week_str = request.GET.get("week")
    if week_str:
        start = date.fromisoformat(week_str)
    else:
        today = date.today()
        start = today - timedelta(days=today.weekday())

    # その週（月曜～日曜）の日付リスト
    week_dates = [start + timedelta(days=i) for i in range(7)]

    # 前週／次週リンク用パラメータ（ISOフォーマット）
    prev_week = (start - timedelta(days=7)).isoformat()
    next_week = (start + timedelta(days=7)).isoformat()

    return render(request, 'student/calendar.html', {
        'week_dates': week_dates,
        'prev_week':  prev_week,
        'next_week':  next_week,
    })
def form_view(request):
    form = StudentForm()
    return render(request, 'student/reserve.html', {'form': form})
