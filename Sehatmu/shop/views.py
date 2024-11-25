from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Produk, Kategori, Keranjang, ItemKeranjang, Pesanan, DetailPesanan

# View untuk daftar produk
def product_list(request):
    categories = Kategori.objects.all()  # Ambil semua kategori
    products = Produk.objects.all()  # Ambil semua produk
    return render(request, 'shop/product_list.html', {'categories': categories, 'products': products})

# View untuk detail produk
def product_detail(request, slug):
    product = get_object_or_404(Produk, slug=slug)  # Ambil produk berdasarkan slug
    return render(request, 'shop/product_detail.html', {'product': product})

# View untuk menambahkan produk ke keranjang
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Produk, id=product_id)  # Ambil produk berdasarkan ID
    cart, created = Keranjang.objects.get_or_create(user=request.user)  # Cari atau buat keranjang untuk pengguna
    cart_item, created = ItemKeranjang.objects.get_or_create(cart=cart, product=product)  # Tambahkan produk ke keranjang
    if not created:
        cart_item.quantity += 1  # Jika sudah ada, tambahkan jumlah
        cart_item.save()
    return redirect('cart_detail')

# View untuk detail keranjang
@login_required
def cart_detail(request):
    cart = Keranjang.objects.get(user=request.user)  # Ambil keranjang milik pengguna
    items = cart.items.all()  # Ambil semua item di keranjang
    total = sum(item.product.price * item.quantity for item in items)  # Hitung total harga
    return render(request, 'shop/cart_detail.html', {'cart': cart, 'items': items, 'total': total})

# View untuk checkout
@login_required
def checkout(request):
    cart = Keranjang.objects.get(user=request.user)  # Ambil keranjang pengguna
    total = sum(item.product.price * item.quantity for item in cart.items.all())  # Hitung total harga
    order = Pesanan.objects.create(user=request.user, total_amount=total)  # Buat pesanan baru
    for item in cart.items.all():
        DetailPesanan.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    cart.items.all().delete()  # Hapus semua item di keranjang setelah checkout
    return render(request, 'shop/order_confirmation.html', {'order': order})

# View untuk menambahkan ulasan produk (jika ada model ulasan)
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Produk, id=product_id)  # Ambil produk berdasarkan ID
    if request.method == 'POST':
        rating = request.POST.get('rating')  # Ambil rating dari form
        comment = request.POST.get('comment')  # Ambil komentar dari form
        # Buat ulasan baru (sesuaikan dengan model ulasan jika ada)
        product.review_set.create(user=request.user, rating=rating, comment=comment)
    return redirect('product_detail', slug=product.slug)