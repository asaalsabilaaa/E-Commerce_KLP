# catalog/models.py
from django.db import models
from django.utils.text import slugify

# Model Kategori
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nama Kategori")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(verbose_name="Deskripsi", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui pada")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Model Product
class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Nama Produk")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(verbose_name="Deskripsi", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Harga")
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products', verbose_name="category")  # Referensi string 'Category' untuk menghindari circular import
    stock_produk = models.PositiveIntegerField(verbose_name="Stok")
    merek_produk = models.CharField(max_length=100, verbose_name="Merek Produk")
    bahan = models.CharField(max_length=100, verbose_name="Bahan Produk", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Produk Aktif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui pada")

    class Meta:
        verbose_name = "Produk"
        verbose_name_plural = "Produk"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Catalog(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # any other fields that should belong to Catalog

    def __str__(self):
        return self.name

class Page(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
