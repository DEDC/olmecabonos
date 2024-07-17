# Django
from django import forms
# app bonos
from .models import Bono, Partidos


class BonosForm(forms.ModelForm):
    class Meta:
        model = Bono
        fields = '__all__'
        
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'})
        }


class PartidosForm(forms.ModelForm):
    class Meta:
        model = Partidos
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'lugar': forms.Select(attrs={'class': 'form-select'})
        }