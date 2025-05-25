from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Brand, Order, OrderItem
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime

def home(request):
    return render(request, 'home.html')

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

@login_required
def view4(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    products = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_price += product.price * quantity
        products.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })

    context = {
        'cart_count': cart_count,
        'cart_items': products,
        'total_price': total_price,
    }
    return render(request, 'view4.html', context)

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'category_detail.html', {'category': category, 'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        cart = request.session.get('cart', {})

        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart

        if action == 'buy':
            messages.success(request, f"Товар '{product.name}' додано до кошика. Перейдіть до оформлення замовлення.")
            return redirect('shop:checkout')
        else:
            messages.success(request, f"Товар '{product.name}' додано до кошика.")
            return redirect('shop:product_detail', product_id=product.id)

    return redirect('shop:product_detail', product_id=product.id)

def cart_detail(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []

    total_price = 0
    for product in products:
        quantity = cart.get(str(product.id), 0)
        subtotal = product.price * quantity
        total_price += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def cart_add(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart
        messages.success(request, "Кількість товару збільшено")
    return redirect('shop:cart_detail')

@login_required
def cart_remove_one(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        quantity = cart.get(str(product_id), 0)
        if quantity > 1:
            cart[str(product_id)] = quantity - 1
            messages.success(request, "Кількість товару зменшено")
        else:
            cart.pop(str(product_id), None)
            messages.success(request, "Товар видалено з кошика")
        request.session['cart'] = cart
    return redirect('shop:cart_detail')

@login_required
def cart_remove(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            cart.pop(str(product_id))
            messages.success(request, "Товар повністю видалено з кошика")
        request.session['cart'] = cart
    return redirect('shop:cart_detail')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.info(request, "Кошик порожній, додайте товари перед оформленням замовлення.")
        return redirect('shop:catalog')

    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total_price = 0
    for product in products:
        quantity = cart.get(str(product.id), 0)
        subtotal = product.price * quantity
        total_price += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_type = request.POST.get('payment_type')
        delivery_type = request.POST.get('delivery_type')
        payment_timing = request.POST.get('payment_timing')

        # Можна додати валідацію тут

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            payment_type=payment_type,
            delivery_type=delivery_type,
            payment_timing=payment_timing,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price,
            )

        # Очистити кошик
        request.session['cart'] = {}
        messages.success(request, f"Дякуємо за замовлення, {full_name}! Ваше замовлення прийняте.")
        return redirect('shop:home')

    now = datetime.now()
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'current_year': now.year,
        'current_month': f"{now.month:02d}",
    }
    return render(request, 'checkout.html', context)
