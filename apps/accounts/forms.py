from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Profile, Document, Machine


class CustomUserCreationForm(UserCreationForm):
    company_name = forms.CharField(
        max_length=200,
        required=False,
        label="Firma / Atölye Adı (opsiyonel)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Firma Adı (opsiyonel)'}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'phone', 'city')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kullanıcı Adı'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-posta Adresi'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ad'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyad'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '05XX XXX XX XX'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Şehir'}),
        }

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.company_name = self.cleaned_data.get('company_name') or ''
            profile.save(update_fields=['company_name'])
        return user


class ProfileUpdateForm(forms.ModelForm):
    """Kullanıcının temel (User) bilgilerini günceller."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'city', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CompanyProfileForm(forms.ModelForm):
    """Firma / atölye bazlı ek bilgileri günceller. is_verified buradan asla elle değiştirilemez."""

    class Meta:
        model = Profile
        fields = ['company_name', 'tax_number', 'address', 'description']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Firma / Atölye Adı'}),
            'tax_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vergi Numarası (opsiyonel)'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Saha / Atölye Adresi'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Kısa açıklama'}),
        }


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'file']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['name', 'quantity', 'note']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: Düz Dikiş Makinesi'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Not (opsiyonel)'}),
        }
