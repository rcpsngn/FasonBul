from django import forms
from .models import Workshop


class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['title', 'category', 'phone', 'city', 'district', 'address', 'capacity']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: XYZ Tekstil Fason Atölyesi'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0555 ...'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: İstanbul'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: Güngören'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Açık adres'}),
            'capacity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: 10.000 Parça / Ay'}),
        }