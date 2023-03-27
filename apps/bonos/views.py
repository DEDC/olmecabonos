# Django
from django.views.generic import CreateView, ListView, RedirectView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
# app bonos
from apps.bonos.models import Bono
from apps.bonos.forms import BonosForm
# utils
from utils.bonos_pdf import generate_bonus

class Registrar(SuccessMessageMixin, CreateView):
    success_message = 'Bono registrado exitosamente'
    model = Bono
    template_name = 'bonos/registro.html'
    form_class = BonosForm
    success_url = reverse_lazy('registro')
    
    def form_valid(self, form):
        abonado = {
            'name': self.request.POST.get('bn-name', 'ND').title(),
            'email': self.request.POST.get('bn-email', 'ND'),
            'phone': self.request.POST.get('bn-phone', 'ND')
        }
        
        bono = {
            'section': self.request.POST.get('bn-section', 'ND').upper(),
            'row': self.request.POST.get('bn-row', 'ND').upper(),
            'seat': self.request.POST.get('bn-seat', 'ND').upper()
        }
        form.instance.abonado = abonado
        form.instance.ubicacion = bono
        self.object = form.save()
        response = generate_bonus([self.object])
        if self.request.POST.get('sv-dw', None) is not None:
            return response
        return super().form_valid(form)

class Listar(ListView):
    model = Bono
    template_name = 'bonos/listado.html'
    
    def get_queryset(self):
        q = self.request.GET.get('q', '')
        lookup = (Q(folio__icontains = q) | Q(abonado__name__icontains = q))
        bonus = self.model._default_manager.filter(lookup)
        self.queryset = bonus
        return bonus
    
    def get_context_data(self):
        context = {'q': self.request.GET.get('q', ''), 'total': self.queryset.count()}
        return super().get_context_data(**context)

class Descargar(RedirectView):
    url = reverse_lazy('listar')
    
    def get(self, request, *args, **kwargs):
        bonus = [request.GET.get('bonus')]
        bonos = Bono.objects.filter(folio__in = bonus)
        response = generate_bonus(bonos)
        try:
            bonos = Bono.objects.filter(folio__in = bonus)
            response = generate_bonus(bonos)
            return response
        except:
            return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        bonus = request.POST.getlist('bonus')
        try:
            bonos = Bono.objects.filter(folio__in = bonus)
            response = generate_bonus(bonos)
            return response
        except:
            return self.get(request, *args, **kwargs)