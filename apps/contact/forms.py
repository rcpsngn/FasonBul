from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adınız Soyadınız'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-posta Adresiniz'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon Numaranız'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mesaj Konusu'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Mesajınız...'}),
        }