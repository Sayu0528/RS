from django.shortcuts import render


def index(request):
    return render(request, 'manager/index.html')

# 出勤者一覧画面
def shift_schedule(request):
    return render(request, 'manager/shift_schedule.html')

#仕事内容入力画面 
def job_explain(request):
    return render(request, 'manager/job_explain.html')

