from django import forms
from .models import Contract


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['quantity', 'unit_price', 'due_date', 'defect_rate', 'extra_terms']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Örn: 5000'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Örn: 12.50'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'defect_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Örn: 2.0'}),
            'extra_terms': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Varsa ek şartlarınızı, kumaş/aksesuar temini gibi detayları buraya yazın...'}),
        }
