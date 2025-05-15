from django.shortcuts import render
from .models import Product  # додай, якщо немає

def home(request):
    products = Product.objects.all()[:12]  # беремо перші 12 товарів
    return render(request, 'home.html', {'products': products})

def view1(request):
    return render(request, 'view1.html')

def view2(request):
    return render(request, 'view2.html')

def view3(request):
    return render(request, 'view3.html')

def view4(request):
    return render(request, 'view4.html')
