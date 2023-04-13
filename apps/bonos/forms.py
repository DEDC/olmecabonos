# Django
from django import forms
# app bonos
from .models import Bono

class BonosForm(forms.ModelForm):
    class Meta:
        model = Bono
        fields = '__all__'
        
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'})
        }