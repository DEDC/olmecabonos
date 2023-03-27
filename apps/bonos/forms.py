# Django
from django.forms import ModelForm
# app bonos
from .models import Bono

class BonosForm(ModelForm):
    class Meta:
        model = Bono
        fields = '__all__'