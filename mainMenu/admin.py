from django.contrib import admin
from django.utils.html import format_html
from .models import Menu, Order, DetailOrder, Supplier, Stok
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('nama_item', 'gambar' , 'kategori', 'harga', 'status')
    list_filter = ('kategori', 'status')
    search_fields = ('nama_item',)
    list_per_page = 5 
    actions = ['print_selected']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('print_selected/', self.admin_site.admin_view(self.print_selected_view), name='menu_print_selected'),
        ]
        return custom_urls + urls

    def print_selected(self, request, queryset):
        ids = queryset.values_list('id_menu', flat=True)
        ids_str = ",".join(str(i) for i in ids)
        return HttpResponseRedirect(f'print_selected/?ids={ids_str}')
    print_selected.short_description = "Print selected items"

    def print_selected_view(self, request):
        ids = request.GET.get('ids')
        if not ids:
            return HttpResponseRedirect("../")  # Redirect ke list if tidak ada id

        ids_list = [int(i) for i in ids.split(",")]
        items = Menu.objects.filter(id_menu__in=ids_list)

        return render(request, 'mainMenu/print_menu.html', {'items': items})

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('nomor_pesanan', 'tanggal', 'nama_customer', 'metode_pembayaran', 'order_mode_display', 'total_harga')
    list_filter = ('metode_pembayaran', 'order_mode', 'tanggal')
    search_fields = ('nomor_pesanan', 'nama_customer')
    ordering = ('-tanggal',)

    def order_mode_display(self, obj):
        return obj.get_order_mode_display()
    order_mode_display.short_description = 'Order Mode'
    list_per_page = 5 
    actions = ['print_selected']

    def order_mode_display(self, obj):
        return obj.get_order_mode_display()
    order_mode_display.short_description = 'Order Mode'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('print_selected/', self.admin_site.admin_view(self.print_selected_view), name='order_print_selected'),
        ]
        return custom_urls + urls

    def print_selected(self, request, queryset):
        ids = queryset.values_list('id_order', flat=True)
        ids_str = ",".join(str(i) for i in ids)
        return HttpResponseRedirect(f'print_selected/?ids={ids_str}')
    print_selected.short_description = "Print selected orders"

    def print_selected_view(self, request):
        ids = request.GET.get('ids')
        if not ids:
            return HttpResponseRedirect("../")
        
        ids_list = [int(i) for i in ids.split(",")]
        items = Order.objects.filter(id_order__in=ids_list)

        return render(request, 'mainMenu/print_order.html', {'items': items})

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('nama_supplier', 'kontak', 'email', 'alamat' , 'jenis_barang', 'status')
    list_filter = ('jenis_barang', 'status')
    search_fields = ('nama_supplier', 'kontak', 'email')
    list_per_page = 5 
    actions = ['print_selected']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('print_selected/', self.admin_site.admin_view(self.print_selected_view), name='supplier_print_selected'),
        ]
        return custom_urls + urls

    def print_selected(self, request, queryset):
        ids = queryset.values_list('id_supplier', flat=True)
        ids_str = ",".join(str(i) for i in ids)
        return HttpResponseRedirect(f'print_selected/?ids={ids_str}')
    print_selected.short_description = "Print selected suppliers"

    def print_selected_view(self, request):
        ids = request.GET.get('ids')
        if not ids:
            return HttpResponseRedirect("../")

        ids_list = [int(i) for i in ids.split(",")]
        items = Supplier.objects.filter(id_supplier__in=ids_list)

        return render(request, 'mainMenu/print_supplier.html', {'items': items})
    
@admin.register(Stok)
class StokAdmin(admin.ModelAdmin):
    list_display = ('bahan_baku', 'jumlah_stok', 'satuan', 'tanggal_update', 'tanggal_kadaluarsa')
    list_filter = ('satuan',)
    search_fields = ('bahan_baku',)
    list_per_page = 5 
    actions = ['print_selected']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('print_selected/', self.admin_site.admin_view(self.print_selected_view), name='stok_print_selected'),
        ]
        return custom_urls + urls

    def print_selected(self, request, queryset):
        ids = queryset.values_list('id_stok', flat=True)
        ids_str = ",".join(str(i) for i in ids)
        return HttpResponseRedirect(f'print_selected/?ids={ids_str}')
    print_selected.short_description = "Print selected stock items"

    def print_selected_view(self, request):
        ids = request.GET.get('ids')
        if not ids:
            return HttpResponseRedirect("../")

        ids_list = [int(i) for i in ids.split(",")]
        items = Stok.objects.filter(id_stok__in=ids_list)

        return render(request, 'mainMenu/print_stok.html', {'items': items})