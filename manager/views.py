from django.shortcuts import render


def index(request):
    return render(request, 'manager/index.html')

# 出勤者一覧画面
def shift_schedule(request):
    return render(request, 'manager/shift_schedule.html')

#仕事内容入力画面 
def job_explain(request):
    return render(request, 'manager/job_explain.html')

#toppage
def toppage(request):
    return render(request, 'manager/toppage.html')

def attendance_list(request):
    """
    出席者名簿ページ
    """
    return render(request, 'manager/attendance_list.html')
