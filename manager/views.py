# manager/views.py

from django.shortcuts import render, redirect
from django.utils import timezone
import datetime
from datetime import timedelta
from collections import defaultdict

from manager.models import ShiftSlot

# ── 定数：週共通の時間帯リスト ──
TIME_SLOTS = [
    "8:00〜9:00",
    "9:00〜10:30",
    "10:40〜12:10",
    "12:10〜13:00",
    "13:00〜14:30",
    "14:45〜16:15",
    "16:30〜18:00",
    "18:15〜19:45",
]


def index(request):
    return render(request, "manager/index.html")


def shift_schedule(request):
    """
    管理者向けの「今週のシフト表」画面。
    ここでは予約者の氏名を一週間分まとめて表示します。
    """
    today = timezone.localdate()
    start = today - timedelta(days=today.weekday())
    week_dates = [start + timedelta(days=i) for i in range(7)]

    slots = (
        ShiftSlot.objects
        .filter(date__range=(week_dates[0], week_dates[-1]))
        .prefetch_related("reservations")
        .order_by("date", "time_slot")
    )

    matrix = defaultdict(dict)
    for s in slots:
        matrix[s.time_slot][s.date] = s

    context = {
        "week_dates": week_dates,
        "time_slots": TIME_SLOTS,
        "matrix": matrix,
    }
    return render(request, "manager/shift_schedule.html", context)


def job_explain(request):
    """
    仕事内容入力画面。
    """
    return render(request, "manager/job_explain.html")


def input_by_date_admin_view(request, date):
    """
    管理者用・日付別の「必要人数入力」画面と保存処理。
    URL 側で '<date>' を渡す（例: /manager/2025-06-05/）。
    """
    # URL から受け取った 'date' は文字列 "YYYY-MM-DD" のはずなので、
    # datetime.date 型に変換してあげる。
    try:
        target_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        # もし 'date' が "2025-06-35" のように不正な文字列なら
        # 404 やリダイレクトを返してもよいですが、ここでは一旦トップに戻します。
        return redirect("calendar_admin")

    if request.method == "POST":
        # フォーム送信時：各時間帯の capacity を更新 or 新規作成
        for idx, slot in enumerate(TIME_SLOTS):
            key = f"slot_{idx}"
            num = request.POST.get(key)
            if num in (None, ""):
                continue
            capacity = int(num)

            shift_obj, created = ShiftSlot.objects.get_or_create(
                date=target_date,
                time_slot=slot,
                defaults={"capacity": capacity}
            )
            if not created:
                shift_obj.capacity = capacity
                shift_obj.update_availability()
                shift_obj.save()

        return redirect("calendar_admin")

    # GET 時：既存データを取得して「フォーム初期値」として渡す
    existing = {
        s.time_slot: s.capacity
        for s in ShiftSlot.objects.filter(date=target_date)
    }

    context = {
        "date": date,               # 表示用に文字列のまま渡す
        "time_slots": TIME_SLOTS,
        "existing": existing,
    }
    return render(request, "manager/input_by_date_admin.html", context)


def calendar_admin_view(request):
    """
    管理者向けの「カレンダー（日付別入力画面）」。
    '?week=0'（今週）、'?week=1'（来週）を切り替えられる例。
    """
    week_offset = int(request.GET.get("week", 0))
    today = timezone.localdate()
    base_date = today + timedelta(weeks=week_offset)
    start = base_date - timedelta(days=base_date.weekday())
    week_dates = [start + timedelta(days=i) for i in range(7)]

    slots = ShiftSlot.objects.filter(date__range=(week_dates[0], week_dates[-1]))
    slot_map = {(s.date, s.time_slot): s for s in slots}

    context = {
        "week_dates": week_dates,
        "time_slots": TIME_SLOTS,
        "slot_map": slot_map,
        "prev_week": week_offset - 1,
        "next_week": week_offset + 1,
    }
    return render(request, "manager/calendar_admin.html", context)
