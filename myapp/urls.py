from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('view1/', views.view1, name='about'),
    path('view2/', views.view2, name='catalog'),
    path('view3/', views.view3, name='support'),
    path('view4/', views.view4, name='profile'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<str:category_name>/', views.category_view, name='category_view'),

]

