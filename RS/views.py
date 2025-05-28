from django.shortcuts import render
from django.http import HttpResponse
# RS/views.py

def toppage(request):
    # トップページを表示
    return render(request, 'toppage.html')

