# Django
from django.views.generic import CreateView, ListView, RedirectView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.contrib import messages
# app bonos
from apps.bonos.models import Bono
from apps.bonos.forms import BonosForm
# utils
from utils.bonos_pdf import generate_bonus, generate_qr
# openpyxl
from openpyxl import load_workbook

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
        if self.request.POST.get('sv-dw', None) is not None:
            response_bn = generate_bonus([self.object])
            return response_bn
        elif self.request.POST.get('sv-qr', None) is not None:
            response_qr = generate_qr(self.object)
            return response_qr
        return HttpResponseRedirect(self.get_success_url())

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
        try:
            bonos = Bono.objects.filter(folio__in = bonus)
            if bonos.exists():
                response = generate_bonus(bonos)
                return response
        except: pass
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        bonus = request.POST.getlist('bonus')
        try:
            bonos = Bono.objects.filter(folio__in = bonus)
            if bonos.exists():
                response = generate_bonus(bonos)
                return response
        except: pass
        return self.get(request, *args, **kwargs)

class CargarExcel(SuccessMessageMixin, TemplateView):
    template_name = 'bonos/carga_excel.html'
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['bonus'] = cache.get('bonus_cache')
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.POST.get('upload') is not None:
            file_ = request.FILES.get('file')
            wb = load_workbook(file_)
            ws = wb.active
            objs = []
            for row in ws.iter_rows(min_row=2):
                abonado = {'name': row[0].value.title(), 'email': '', 'phone': ''}
                bono = {'section': str(row[1].value).upper(), 'row': row[2].value.upper(), 'seat': str(row[3].value).upper()}
                objs.append(Bono(abonado=abonado, ubicacion=bono, tipo=row[4].value))
            cache.set('bonus_cache', objs)
        if request.POST.get('save') is not None:
            bonus_saved = Bono.objects.bulk_create(cache.get('bonus_cache'))
            messages.success(self.request, 'Se registraron {} bono(s) exitosamente'.format(len(bonus_saved)))
            cache.set('bonus_cache', [])
        context['bonus'] = cache.get('bonus_cache')
        return self.render_to_response(context)