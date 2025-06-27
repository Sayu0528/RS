from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import date, timedelta
from django.views import View
from .forms import StudentForm
from .models import Reservation
from manager.models import ShiftSlot
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.urls import reverse

# Create your views here.
TIME_SLOTS = [
    "8:00〜9:00", "9:00〜10:30", "10:40〜12:10",
    "12:10〜13:00", "13:00〜14:30", "14:45〜16:15",
    "16:30〜18:00", "18:15〜19:45",
]
# 入力情報確認画面
def confirm_form(request):
    return render(request, 'student/confirm_form.html')

#送信完了画面
def trans_comp(request):
    return render(request, 'student/trans_comp.html')

def calendar_view(request):
    # 今日の日付を常に取得しておく
    today = date.today()

    # 「week=YYYY-MM-DD」の GET パラメータがあればその週の月曜を start に
    week_str = request.GET.get("week")
    if week_str:
        # パラメータ指定時も today は変えずに使う
        start = date.fromisoformat(week_str)
    else:
        # 今週の月曜
        start = today - timedelta(days=today.weekday())

    # 週の日付リスト
    week_dates = [start + timedelta(days=i) for i in range(7)]
    prev_week = (start - timedelta(days=7)).isoformat()
    next_week = (start + timedelta(days=7)).isoformat()

    # その週の「空きがある」＆「今日以降」の ShiftSlot を取得
    slots = ShiftSlot.objects.filter(
        date__range=(week_dates[0], week_dates[-1]),
        is_available=True,
        date__gte=today,
    )

    # キーを "YYYY-MM-DD@時間帯" の文字列にして辞書化
    slot_map = {
        f"{s.date.isoformat()}@{s.time_slot}": s
        for s in slots
    }

    return render(request, "student/calendar.html", {
        "today": today,
        "week_dates": week_dates,
        "time_slots": TIME_SLOTS,
        "slot_map": slot_map,
        "prev_week": prev_week,
        "next_week": next_week,
    })

def form_view(request):
    slot_id = request.GET.get("slot")
    if slot_id and slot_id.isdigit():
        slot_id = int(slot_id)
    initial = {"shift_slot": slot_id} if slot_id else None

    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            slot = form.cleaned_data["shift_slot"]
            if slot.remaining == 0:
                form.add_error("shift_slot", "この枠は満席になりました")
            else:
                Reservation.objects.create(
                    student_name=form.cleaned_data["name"],
                    student_id=form.cleaned_data["student_id"],
                    student_email=form.cleaned_data["email"],
                    shift_slot=slot,
                )
                return redirect("trans_comp")
    else:
        form = StudentForm(initial=initial)

    return render(request, "student/reserve.html", {"form": form})

def my_reservations_form(request):
    """
    ユーザーが自分の名前を入力するフォームを表示します。
    GET リクエストでこのページにアクセスするとレンダリングされる想定です。
    """
    return render(request, "student/my_reservations_form.html")


# ── 〔2/3〕検索結果を表示するビュー ──
def my_reservations(request):
    searched_id = request.POST.get("student_id", "").strip()
    searched_name = request.POST.get("student_name", "").strip()

    # 何も入力がなければフォーム再表示＋エラー
    if request.method == "POST" and not (searched_id or searched_name):
        return render(request, "student/my_reservations_form.html", {
            "error": "学籍番号かお名前のいずれかを入力してください。",
        })

    reservations = []
    if request.method == "POST":
        qs = Reservation.objects.select_related("shift_slot")
        if searched_id:
            qs = qs.filter(student_id=searched_id)
        if searched_name:
            qs = qs.filter(student_name__icontains=searched_name)
        reservations = qs.order_by("-created_at")

    return render(request, "student/my_reservations.html", {
        "searched_id": searched_id,
        "searched_name": searched_name,
        "reservations": reservations,
    })



@require_POST
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    name = reservation.student_name
    reservation.delete()

    # キャンセル後に再度検索結果を表示したい場合:
    from .models import Reservation as Res
    results = Res.objects.filter(student_name=name).order_by("slot__date", "slot__time_slot")
    return render(request, "student/my_reservations.html", {
        "reservations": results,
        "searched_name": name,
    })

def base(request):
    return render(request, 'student/calendar_base.html')


def my_reservation_cancel(request, pk):
    # student_id フィールドにユーザーの PK を保存しているなら…
    reservation = get_object_or_404(
        Reservation,
        pk=pk,)
        
    if request.method == "POST":
        reservation.delete()
    return redirect("my_reservations_form")