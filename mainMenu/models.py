from xml.dom import ValidationErr
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  

class Menu(models.Model):
    KATEGORI_CHOICES = [
        ('snack', 'Snack'),
        ('pastry', 'Pastry'),
        ('cake', 'Cake'),
        ('coffee', 'Coffee'),
        ('non_coffee', 'Non Coffee'),
    ]

    id_menu = models.AutoField(primary_key=True)
    nama_item = models.CharField(max_length=100)
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES)
    gambar = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.nama_item

class Order(models.Model):
    METODE_PEMBAYARAN_CHOICES = [
        ('Cash', 'Cash'),
        ('Debit', 'Debit'),
        ('Qris', 'Qris'),
    ]

    ORDER_MODE_CHOICES = [
    ('Dine-in', 'Dine-in'),
    ('Takeaway', 'Takeaway'),
    ]

    id_order = models.AutoField(primary_key=True)  
    nomor_pesanan = models.CharField(max_length=20, unique=True)  
    tanggal = models.DateTimeField(auto_now_add=True) 
    nama_customer = models.CharField(max_length=100, blank=True, null=True) 
    total_harga = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    metode_pembayaran = models.CharField(max_length=10, choices=METODE_PEMBAYARAN_CHOICES)
    order_mode = models.CharField(max_length=10, choices=ORDER_MODE_CHOICES)
    kasir = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nomor_pesanan} - {self.nama_customer or 'Tanpa Nama'}"

    def hitung_total(self):
        # hitung total dr detail order
        total = sum(item.subtotal for item in self.detail_orders.all())
        self.total_harga = total
        self.save()

    @staticmethod
    def generate_nomor_pesanan():
        today = timezone.now().date()
        count_today = Order.objects.filter(tanggal__date=today).count() + 1
        return f"ORD-{today.strftime('%Y%m%d')}-{count_today:03}"
    
    @property
    def total_item(self):
        return sum(item.jumlah_item for item in self.detail_orders.all())

    
class DetailOrder(models.Model):
    id_detailOrder = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='detail_orders')
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True)
    jumlah_item = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Hitung subtotal 
        if self.menu:
            self.subtotal = self.menu.harga * self.jumlah_item
        super().save(*args, **kwargs)

    def clean(self):
        if self.jumlah_item <= 0:
            raise ValidationErr("Jumlah item harus lebih dari 0.")

    def __str__(self):
        return f"{self.jumlah_item} x {self.menu.nama_item} (Order #{self.order.id_order})"
    

class Supplier(models.Model):
    JENIS_BARANG_CHOICES = [
        ('makanan', 'Bahan Baku Makanan'),
        ('minuman', 'Bahan Baku Minuman'),
        ('kemasan', 'Kemasan Pakai'),
        ('pendukung', 'Barang Pendukung'),
    ]

    id_supplier = models.AutoField(primary_key=True)
    nama_supplier = models.CharField(max_length=100)
    kontak = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    alamat = models.TextField()
    jenis_barang = models.CharField(max_length=20, choices=JENIS_BARANG_CHOICES)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.nama_supplier

class Stok(models.Model):
    SATUAN_CHOICES = [
        ('gram', 'Gram'),
        ('liter', 'Liter'),
        ('pack', 'Pack'),
        ('bottle', 'Bottle'),
    ]

    id_stok = models.AutoField(primary_key=True)
    bahan_baku = models.CharField(max_length=100)
    satuan = models.CharField(max_length=10, choices=SATUAN_CHOICES)
    jumlah_stok = models.PositiveIntegerField()
    tanggal_update = models.DateField(default=timezone.now)
    tanggal_kadaluarsa = models.DateField()

    def __str__(self):
        return f"{self.bahan_baku} ({self.jumlah_stok} {self.satuan})"