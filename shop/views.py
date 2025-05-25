from django.shortcuts import render, get_object_or_404
from .models import Category
from .models import Product, Brand
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
def home(request):
    return render(request, 'home.html')  # Без товарів

def view1(request):
    return render(request, 'view1.html')

def view2(request):
    products = Product.objects.all()
    brands = Brand.objects.all()

    selected_brand = request.GET.get('brand')
    if selected_brand:
        products = products.filter(brand__name__iexact=selected_brand)


    search_query = request.GET.get('search', '').strip()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    return render(request, 'view2.html', {'products': products, 'brands': brands})

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

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)] += 1
        else:
            cart[str(product_id)] = 1

        request.session['cart'] = cart

        if action == 'buy':
            # Перенаправити на кошик для оформлення замовлення
            messages.success(request, f"Товар '{product.name}' додано до кошика. Ви можете оформити замовлення.")
            return redirect('shop:view4')  # Припустимо, тут особистий кабінет з кошиком
        else:
            messages.success(request, f"Товар '{product.name}' додано до кошика.")
            return redirect('shop:product_detail', product_id=product.id)
    else:
        return redirect('shop:product_detail', product_id=product.id)
