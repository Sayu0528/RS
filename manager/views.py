# manager/views.py

from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime, date, timedelta
from collections import defaultdict

from .models import ShiftSlot

TIME_SLOTS = [
    "8:00〜9:00", "9:00〜10:30", "10:40〜12:10",
    "12:10〜13:00", "13:00〜14:30", "14:45〜16:15",
    "16:30〜18:00", "18:15〜19:45",
]

def home_design(request):
    releases = [
        {"date": "2025.06.10", "title": "銀聯決済でサイン...", "url": "#"},
        {"date": "2025.05.07", "title": "システム修正 ver.1.5.6", "url": "#"},
        {"date": "2025.04.28", "title": "システム修正 ver.1.5.1", "url": "#"},
    ]
    services = [
        {"name": "券売機",           "icon": "manager/images/icon_ticket.svg",  "active": True,  "setting_url": "#"},
        {"name": "モバイルオーダー", "icon": "manager/images/icon_mobile.svg",  "active": False, "setting_url": None},
    ]
    return render(request, "manager/home.html", {"releases": releases, "services": services})

def index(request):
    return render(request, "manager/index.html")

def job_explain(request):
    return render(request, "manager/job_explain.html")

def get_week_start(d):
    return d - timedelta(days=d.weekday())

def calendar_admin_view(request):
    week_str = request.GET.get("week")
    try:
        base = datetime.strptime(week_str, "%Y-%m-%d").date() if week_str else timezone.localdate()
    except (ValueError, TypeError):
        base = timezone.localdate()
    start = get_week_start(base)
    week_dates = [start + timedelta(days=i) for i in range(7)]
    prev_week = (start - timedelta(days=7)).strftime("%Y-%m-%d")
    next_week = (start + timedelta(days=7)).strftime("%Y-%m-%d")
    return render(request, "manager/calendar_admin.html", {
        "week_dates": week_dates,
        "prev_week":  prev_week,
        "next_week":  next_week,
        "time_slots": TIME_SLOTS,
    })

def input_by_date_admin_view(request, date):
    try:
        target = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return redirect("manager:admin_calendar")
    if request.method == "POST":
        for idx, slot in enumerate(TIME_SLOTS):
            val = request.POST.get(f"slot_{idx}")
            if not val: continue
            obj, created = ShiftSlot.objects.get_or_create(
                date=target, time_slot=slot, defaults={"capacity": int(val)}
            )
            if not created:
                obj.capacity = int(val)
                obj.update_availability()
                obj.save()
        return redirect(request.path)
    existing = {s.time_slot: s.capacity for s in ShiftSlot.objects.filter(date=target)}
    return render(request, "manager/input_by_date_admin.html", {
        "date":       date,
        "time_slots": TIME_SLOTS,
        "existing":   existing,
    })

def shift_schedule(request):
    today = timezone.localdate()
    start = today - timedelta(days=today.weekday())
    week_dates = [start + timedelta(days=i) for i in range(7)]
    slots = (ShiftSlot.objects
             .filter(date__range=(week_dates[0], week_dates[-1]))
             .prefetch_related("reservations")
             .order_by("time_slot", "date"))
    matrix = defaultdict(dict)
    for s in slots:
        matrix[s.time_slot][s.date] = s
    return render(request, "manager/shift_schedule.html", {
        "week_dates": week_dates,
        "time_slots": TIME_SLOTS,
        "matrix":     matrix,
    })
