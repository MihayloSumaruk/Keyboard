from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def view1(request):
    return render(request, "view1.html")

def view2(request):
    return render(request, "view2.html")

def view3(request):
    return render(request, "view3.html")

def view4(request):
    return render(request, "view4.html")
