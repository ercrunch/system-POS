from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import MenuForm
from .models import Menu, Order, DetailOrder


def index(request):
    return render(request, 'index.html')


# Login Kasir
def kasir_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.groups.filter(name='Kasir').exists():
                login(request, user)
                return redirect('kasir_dashboard')
            else:
                return render(request, 'login.html', {'error': 'Akun ini bukan kasir.'})
        else:
            return render(request, 'login.html', {'error': 'Username atau password salah.'})

    return render(request, 'login.html')


# Dashboard Kasir
@login_required
def kasir_dashboard(request):
    user = request.user

    total_menu = Menu.objects.count()
    today = timezone.now().date()
    jumlah_pesanan_hari_ini = Order.objects.filter(tanggal__date=today).count()
    pendapatan_hari_ini = Order.objects.filter(tanggal__date=today).aggregate(
        total=Sum('total_harga')
    )['total'] or 0

    menu_sold_out = Menu.objects.filter(status=False)

    context = {
        'user': user,
        'total_menu': total_menu,
        'jumlah_pesanan_hari_ini': jumlah_pesanan_hari_ini,
        'pendapatan_hari_ini': pendapatan_hari_ini,
        'menu_sold_out': menu_sold_out,
    }
    return render(request, 'kasir/dashboard.html', context)


# Order Kasir
@login_required
def kasir_order(request):
    search_query = request.GET.get('search', '')
    kategori = request.GET.get('kategori', '')

    menus = Menu.objects.filter(status=True)

    if kategori and kategori != "All":
        menus = menus.filter(kategori=kategori)

    if search_query:
        menus = menus.filter(nama_item__icontains=search_query)

    context = {
        'user': request.user,
        'menus': menus,
        'kategori': kategori,
        'search': search_query,
    }
    return render(request, 'kasir/order.html', context)


# Checkout Order
@csrf_exempt
@login_required
def checkout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'JSON tidak valid'})

        order_items = data.get('orderItems')
        metode_pembayaran = data.get('metode_pembayaran', 'Cash')
        order_mode = data.get('order_mode', 'Dine In')
        nama_customer = data.get('nama_customer', '')

        if not order_items:
            return JsonResponse({'success': False, 'error': 'Order kosong'})

        nomor_pesanan = Order.generate_nomor_pesanan()

        order = Order.objects.create(
            nomor_pesanan=nomor_pesanan,
            metode_pembayaran=metode_pembayaran,
            kasir=request.user,
            total_harga=0,
            nama_customer=nama_customer,
            order_mode=order_mode,
        )

        total = 0
        for item in order_items:
            try:
                menu = Menu.objects.get(id_menu=item['id_menu'])
            except Menu.DoesNotExist:
                continue

            jumlah_item = item.get('jumlah_item', 0)
            subtotal = menu.harga * jumlah_item

            DetailOrder.objects.create(
                order=order,
                menu=menu,
                jumlah_item=jumlah_item,
                subtotal=subtotal,
            )
            total += subtotal

        order.total_harga = total
        order.save()

        return JsonResponse({'success': True, 'nomor_pesanan': nomor_pesanan})

    return JsonResponse({'success': False, 'error': 'Metode tidak valid'})


# Summary Transaction Kasir
@login_required
def kasir_summary(request):
    filter_param = request.GET.get('filter', 'all') 
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())

    if filter_param == "today":
        orders = Order.objects.filter(tanggal__date=today)
    elif filter_param == "week":
        orders = Order.objects.filter(tanggal__date__gte=start_of_week)
    else:
        orders = Order.objects.all()

    orders = orders.prefetch_related('detail_orders__menu').order_by('-tanggal')

    return render(request, 'kasir/summary.html', {'orders': orders})


# ADMIN
# Tambah Menu
def tambah_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('daftar_menu')
    else:
        form = MenuForm()

    return render(request, 'mainMenu/tambah_menu.html', {'form': form})


# Daftar Menu
def daftar_menu(request):
    menus = Menu.objects.all()
    return render(request, 'mainMenu/daftar_menu.html', {'menus': menus})
