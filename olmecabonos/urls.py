# Djanfo
from django.urls import path
from apps.bonos.views import Registrar, Listar, Descargar, CargarExcel

urlpatterns = [
    path('', Registrar.as_view(), name='registro'),
    path('bonos', Listar.as_view(), name='listar'),
    path('bonos/descargar', Descargar.as_view(), name='descargar'),
    path('bonos/cargar-excel', CargarExcel.as_view(), name='cargar')
]