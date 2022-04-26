# Django
from django.views.generic import TemplateView
# app bonos
from apps.bonos.models import Bono
# utils
from utils.bonos_pdf import generate_bonus

class Main(TemplateView):
    template_name = 'bonos/registro.html'

def download_bonus(request):
    # bono = Bono.objects.filter(tipo='comprado')
    bono = Bono.objects.filter(fecha_reg__day=26, fecha_reg__month=4, fecha_reg__year=2022)
    print(bono)
    return generate_bonus(bono)