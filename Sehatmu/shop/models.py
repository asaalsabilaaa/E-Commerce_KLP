from django.db import models
from django.utils.text import slugify
from accounts.models import User  # Menggunakan model User kustom dari aplikasi accounts


# Model Kategori (One-to-Many)
class Kategori(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Nama Kategori")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(verbose_name="Deskripsi", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui pada")

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategori"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Model Produk (One-to-Many dengan Kategori)
class Produk(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Nama Produk")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(verbose_name="Deskripsi", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Harga")
    category = models.ForeignKey(Kategori, on_delete=models.CASCADE, related_name='products', verbose_name="Kategori")
    stock_produk = models.PositiveIntegerField(verbose_name="Stok")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui pada")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")

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


# Model Keranjang Belanja (Many-to-Many dengan Model Penghubung)
class Keranjang(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Pengguna")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat pada")

    class Meta:
        verbose_name = 'Keranjang'
        verbose_name_plural = 'Keranjang'

    def __str__(self):
        return f"Keranjang {self.id} milik {self.user.username}"


class ItemKeranjang(models.Model):
    cart = models.ForeignKey(Keranjang, on_delete=models.CASCADE, related_name='items', verbose_name="Keranjang")
    product = models.ForeignKey(Produk, on_delete=models.CASCADE, verbose_name="Produk")
    quantity = models.PositiveIntegerField(verbose_name="Jumlah")

    class Meta:
        verbose_name = 'Item Keranjang'
        verbose_name_plural = 'Item Keranjang'

    def __str__(self):
        return f"{self.quantity} x {self.product.name} di Keranjang {self.cart.id}"


# Model Pesanan (Many-to-Many)
class Pesanan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Pengguna")
    products = models.ManyToManyField(Produk, through='DetailPesanan', related_name='orders', verbose_name="Produk")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Harga")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal Pesanan")
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Menunggu'),
            ('SHIPPED', 'Dikirim'),
            ('DELIVERED', 'Diterima'),
        ],
        default='PENDING',
        verbose_name="Status"
    )

    class Meta:
        verbose_name = 'Pesanan'
        verbose_name_plural = 'Pesanan'

    def __str__(self):
        return f"Pesanan {self.id} oleh {self.user.username}"


# Model Detail Pesanan (One-to-Many)
class DetailPesanan(models.Model):
    order = models.ForeignKey(Pesanan, on_delete=models.CASCADE, related_name='details', verbose_name="Pesanan")
    product = models.ForeignKey(Produk, on_delete=models.CASCADE, verbose_name="Produk")
    quantity = models.PositiveIntegerField(verbose_name="Jumlah")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Harga")

    class Meta:
        verbose_name = 'Detail Pesanan'
        verbose_name_plural = 'Detail Pesanan'

    def __str__(self):
        return f"{self.quantity} x {self.product.name} di Pesanan {self.order.id}"