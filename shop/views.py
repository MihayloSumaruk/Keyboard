from django.shortcuts import render, get_object_or_404
from .models import Product
from .models import Category, Product
def home(request):
    products = Product.objects.all()[:12]  # беремо перші 12 товарів
    return render(request, 'home.html', {'products': products})

def view1(request):
    return render(request, 'view1.html')

def view2(request):
    products = Product.objects.all()
    return render(request, 'view2.html', {'products': products})
def view3(request):
    return render(request, 'view3.html')

def view4(request):
    return render(request, 'view4.html')

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'category_detail.html', {'category': category, 'products': products})
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})