from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.view1, name='about'),
    path('catalog/', views.view2, name='catalog'),
    path('support/', views.view3, name='support'),
    path('profile/', views.view4, name='profile'),

    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # кошик
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove_one/<int:product_id>/', views.cart_remove_one, name='cart_remove_one'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
