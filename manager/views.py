from django.shortcuts import render

# Create your views here.

def calendar_admin_view(request):
    import datetime
    today = datetime.date.today()
    start = today - datetime.timedelta(days=today.weekday())
    week_dates = [start + datetime.timedelta(days=i) for i in range(7)]

    time_slots = [
        "8:00〜9:00", "9:00〜10:30", "10:40〜12:10",
        "12:10〜13:00", "13:00〜14:30", "14:45〜16:15",
        "16:30〜18:00", "18:15〜19:45"
    ]

    return render(request, 'calendar_admin.html', {
        'week_dates': week_dates,
        'time_slots': time_slots,
    })

# ── 管理者用 日付別入力画面 ──
def input_by_date_admin_view(request, date):
    time_slots = [
        "8:00〜9:00", "9:00〜10:30", "10:40〜12:10",
        "12:10〜13:00", "13:00〜14:30", "14:45〜16:15",
        "16:30〜18:00", "18:15〜19:45"
    ]
    return render(request, 'input_by_date_admin.html', {
        'date': date,
        'time_slots': time_slots,
    })