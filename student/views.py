from django.shortcuts import render

# Create your views here.

# 入力情報確認画面
def confirm_form(request):
    return render(request, 'student/confirm_form.html')

#送信完了画面
def trans_comp(request):
    return render(request, 'student/trans_comp.html')