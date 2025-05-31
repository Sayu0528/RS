from django import forms
from manager.models import ShiftSlot

class StudentForm(forms.Form):
    name = forms.CharField(label='名前', max_length=100)
    student_id = forms.CharField(label='学籍番号', max_length=20)
    email = forms.EmailField(label='メールアドレス')
    shift_slot = forms.ModelChoiceField(
    label="予約枠（日時）",
    queryset=ShiftSlot.objects.filter(is_available=True).order_by("date", "time_slot"),
    empty_label="選択してください",
)