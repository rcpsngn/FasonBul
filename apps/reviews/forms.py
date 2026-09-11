from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'workmanship_score', 'timeliness_score',
            'payment_discipline_score', 'defect_rate_score', 'comment',
        ]
        widgets = {
            'workmanship_score': forms.RadioSelect,
            'timeliness_score': forms.RadioSelect,
            'payment_discipline_score': forms.RadioSelect,
            'defect_rate_score': forms.RadioSelect,
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Varsa eklemek istediğiniz notlar...'}),
        }
