# manager/views.py

from django.shortcuts import render, redirect   # ← redirect を追加
import datetime                                 # ← datetime を追加
from manager.models import ShiftSlot            # ← ShiftSlot モデルをインポート
# ※ TIME_SLOTS はモデル側に置いた場合はインポート可能
#    ここではビューで直接定義します。

# 1週間で共通に使う時間帯リストを定数化
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
    return render(request, 'manager/index.html')

# 出勤者一覧画面
def shift_schedule(request):
    return render(request, 'manager/shift_schedule.html')

# 仕事内容入力画面
def job_explain(request):
    return render(request, 'manager/job_explain.html')

def calendar_admin_view(request):
    # 今日の日付から今週（月曜開始の日付リスト）を計算
    today = datetime.date.today()
    start = today - datetime.timedelta(days=today.weekday())
    week_dates = [start + datetime.timedelta(days=i) for i in range(7)]

    # 今週の予約枠をすべて取得（空き状況に関係なく）
    slots = ShiftSlot.objects.filter(
        date__range=(week_dates[0], week_dates[-1])
    )
    # (date, time_slot) のタプルをキーにして ShiftSlot を辞書化
    slot_map = {(s.date, s.time_slot): s for s in slots}

    return render(request, "manager/calendar_admin.html", {
        "week_dates": week_dates,
        "time_slots": TIME_SLOTS,
        "slot_map": slot_map,
    })

# ── 管理者用 日付別入力画面 ──
def input_by_date_admin_view(request, date):
    # URL パラメータ date は文字列 "YYYY-MM-DD" なので日付型に変換
    target_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

    if request.method == "POST":
        # フォーム送信時：各時間帯の必要人数を保存／更新
        for idx, slot in enumerate(TIME_SLOTS):
            key = f"slot_{idx}"
            num = request.POST.get(key)
            # 空欄のままならスキップ
            if num is None or num == "":
                continue

            capacity = int(num)
            # 既存なら取得、新規なら作成（capacity は defaults でセット）
            shift, created = ShiftSlot.objects.get_or_create(
                date=target_date,
                time_slot=slot,
                defaults={"capacity": capacity}
            )
            # 既存レコードなら capacity を更新
            if not created:
                shift.capacity = capacity
                shift.update_availability()  # 残枠に合わせて is_available を更新
                shift.save()

        # 保存後は管理者カレンダーページにリダイレクト
        return redirect("admin_calendar")

    # GET 時：初期表示として、既存の各枠の capacity を辞書にして渡す
    existing = {
        s.time_slot: s.capacity
        for s in ShiftSlot.objects.filter(date=target_date)
    }

    return render(request, "manager/input_by_date_admin.html", {
        "date": date,
        "time_slots": TIME_SLOTS,
        "existing": existing,
    })
