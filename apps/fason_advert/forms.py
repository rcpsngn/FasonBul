from django import forms
from .models import Advert


class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = ['title', 'category', 'advert_type', 'description', 'city', 'district', 'quantity', 'price', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: 5000 Adet Örme Penye Dikim İşi'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'advert_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'İlan detaylarını ve şartlarınızı giriniz...'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: İstanbul'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: Zeytinburnu'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Adet sayısı'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Birim fiyat (isteğe bağlı)'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }