from django.contrib import admin
from .models import Kategori, Produk, Keranjang, ItemKeranjang, Pesanan, DetailPesanan

admin.site.register(Kategori)
admin.site.register(Produk)
admin.site.register(Keranjang)
admin.site.register(ItemKeranjang)
admin.site.register(Pesanan)
admin.site.register(DetailPesanan)