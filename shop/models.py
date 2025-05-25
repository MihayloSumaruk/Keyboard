from django.db import models

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
