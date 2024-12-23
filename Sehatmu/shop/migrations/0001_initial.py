# Generated by Django 5.1.2 on 2024-11-25 13:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kategori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Nama Kategori')),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Deskripsi')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Dibuat pada')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Diperbarui pada')),
            ],
            options={
                'verbose_name': 'Kategori',
                'verbose_name_plural': 'Kategori',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Keranjang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Dibuat pada')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Pengguna')),
            ],
            options={
                'verbose_name': 'Keranjang',
                'verbose_name_plural': 'Keranjang',
            },
        ),
        migrations.CreateModel(
            name='Pesanan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total Harga')),
                ('order_date', models.DateTimeField(auto_now_add=True, verbose_name='Tanggal Pesanan')),
                ('status', models.CharField(choices=[('PENDING', 'Menunggu'), ('SHIPPED', 'Dikirim'), ('DELIVERED', 'Diterima')], default='PENDING', max_length=20, verbose_name='Status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Pengguna')),
            ],
            options={
                'verbose_name': 'Pesanan',
                'verbose_name_plural': 'Pesanan',
            },
        ),
        migrations.CreateModel(
            name='DetailPesanan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Jumlah')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Harga')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='shop.pesanan', verbose_name='Pesanan')),
            ],
            options={
                'verbose_name': 'Detail Pesanan',
                'verbose_name_plural': 'Detail Pesanan',
            },
        ),
        migrations.CreateModel(
            name='Produk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Nama Produk')),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Deskripsi')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Harga')),
                ('stock_produk', models.PositiveIntegerField(verbose_name='Stok')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Dibuat pada')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Diperbarui pada')),
                ('is_active', models.BooleanField(default=True, verbose_name='Aktif')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.kategori', verbose_name='Kategori')),
            ],
            options={
                'verbose_name': 'Produk',
                'verbose_name_plural': 'Produk',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='pesanan',
            name='products',
            field=models.ManyToManyField(related_name='orders', through='shop.DetailPesanan', to='shop.produk', verbose_name='Produk'),
        ),
        migrations.CreateModel(
            name='ItemKeranjang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Jumlah')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shop.keranjang', verbose_name='Keranjang')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.produk', verbose_name='Produk')),
            ],
            options={
                'verbose_name': 'Item Keranjang',
                'verbose_name_plural': 'Item Keranjang',
            },
        ),
        migrations.AddField(
            model_name='detailpesanan',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.produk', verbose_name='Produk'),
        ),
    ]
