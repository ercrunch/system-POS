from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'), 
    path('login/', views.kasir_login, name='login'),  
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  

    # Kasir-related
    path('dashboard/', views.kasir_dashboard, name='kasir_dashboard'),  
    path('order/', views.kasir_order, name='kasir_order'),             
    path('summary/', views.kasir_summary, name='kasir_summary'),       

    # Menu
    path('menu/', views.daftar_menu, name='daftar_menu'),              
    path('menu/tambah/', views.tambah_menu, name='tambah_menu'),     

    # Checkout
    path('checkout/', views.checkout, name='checkout'),
]
