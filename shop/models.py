from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name="Назва категорії"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Slug категорії"
    )

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Бренд")

    def __str__(self):
        return self.name


class Product(models.Model):
    MEMBRANIK = 'MEMBRANIK'
    MECHANIK = 'MECHANIK'

    PRODUCT_TYPE_CHOICES = [
        (MEMBRANIK, 'Мембранні'),
        (MECHANIK, 'Механічні'),
    ]

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        verbose_name="Зображення"
    )

    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name="Категорія"
    )
    brand = models.ForeignKey(
        Brand,
        related_name='products',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Бренд"
    )
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name="Назва товару"
    )
    slug = models.SlugField(
        max_length=200,
        db_index=True,
        verbose_name="Slug товару"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Опис"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Ціна"
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Кількість на складі"
    )
    available = models.BooleanField(
        default=True,
        verbose_name="Доступність"
    )
    product_type = models.CharField(
        max_length=50,
        choices=PRODUCT_TYPE_CHOICES,
        default=MECHANIK,
        verbose_name="Тип товару"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення"
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата оновлення"
    )

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Готівка'),
        ('card', 'Карта'),
    ]
    DELIVERY_CHOICES = [
        ('courier', 'Кур’єр'),
        ('pickup', 'Самовивіз'),
    ]
    PAYMENT_TIMING_CHOICES = [
        ('prepay', 'Перед оплатою'),
        ('on_delivery', 'При отриманні товару'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    delivery_type = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
    payment_timing = models.CharField(max_length=15, choices=PAYMENT_TIMING_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Замовлення {self.id} від {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.price * self.quantity
