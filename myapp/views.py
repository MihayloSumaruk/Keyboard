from django.http import HttpResponse

def home(request):
    return HttpResponse("Home from myapp")

def view1(request):
    return HttpResponse("About from myapp")

def view2(request):
    return HttpResponse("Catalog from myapp")

def view3(request):
    return HttpResponse("Support from myapp")

def view4(request):
    return HttpResponse("Profile from myapp")
