# shop/models.py
from django.db import models

# Model Product (di sini kita akan menggunakan referensi string untuk menghindari circular import)
class Product(models.Model):
    category = models.ForeignKey('catalog.Category', on_delete=models.CASCADE)  # Referensi string untuk 'Category'
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
