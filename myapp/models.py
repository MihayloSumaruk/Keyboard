from django.db import models

class Product(models.Model):
    model = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    # інші поля, наприклад ціна, опис тощо

    def __str__(self):
        return f"{self.brand} {self.model}"
