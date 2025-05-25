from django.urls import path
from shop import views as shop_views  # Імпортуємо view з shop

app_name = 'shop'  # namespace для URL

urlpatterns = [
    path('', shop_views.home, name='home'),
    path('view1/', shop_views.view1, name='about'),
    path('view2/', shop_views.view2, name='catalog'),
    path('view3/', shop_views.view3, name='support'),
    path('view4/', shop_views.view4, name='profile'),
    path('product/<int:product_id>/', shop_views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', shop_views.category_detail, name='category_detail'),
    path('add-to-cart/<int:product_id>/', shop_views.add_to_cart, name='add_to_cart'),
]
