from django.shortcuts import render


def index(request):
    return render(request, 'manager/index.html')

def shift_schedule(request):
    return render(request, 'manager/shift_schedule.html')

