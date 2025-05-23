from django.shortcuts import render
from django.http import HttpResponse
from datetime import date, timedelta
from django.views import View
# RS/views.py

def toppage(request):
    # トップページを表示
    return render(request, 'toppage.html')

def calendar_view(request):
    start = date.today() - timedelta(days=date.today().weekday())
    week_dates = [start + timedelta(days=i) for i in range(7)]
    
    time_slots = [
        {"label": "8:00〜9:00", "key": "slot1"},
        {"label": "9:00〜10:30", "key": "slot2"},
        # ... さらに6スロット
    ]
    
    availability = {
        d: {ts["key"]: d.weekday() < 5 for ts in time_slots}
        for d in week_dates
    }

    return render(request, "calendar.html", {
        "current_date": start,
        "week_dates": week_dates,
        "prev_week": (start - timedelta(days=7)).isoformat(),
        "next_week": (start + timedelta(days=7)).isoformat(),
        "time_slots": time_slots,
        "availability": availability
    })
