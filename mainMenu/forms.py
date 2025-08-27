from django import forms
from .models import Menu

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['nama_item', 'kategori', 'gambar', 'harga', 'status']
