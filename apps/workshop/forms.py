from django import forms
from .models import Workshop


class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = [
            'title', 'category', 'phone', 'email', 'employee_count',
            'daily_capacity', 'city', 'district', 'address',
            'description', 'logo', 'cover_image', 'capacity',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: XYZ Tekstil Fason Atölyesi'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0555 ...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ornek@atolye.com'}),
            'employee_count': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'daily_capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Örn: 500'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: İstanbul'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: Güngören'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Açık adres'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Uzmanlık alanlarınızı kısaca anlatın'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'capacity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: 10.000 Parça / Ay'}),
        }