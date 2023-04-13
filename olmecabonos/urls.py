# Django
from django.urls import path
from apps.bonos.views import Registrar, Listar, Descargar, CargarExcel, Editar, Eliminar

urlpatterns = [
    path('', Registrar.as_view(), name='registro'),
    path('bonos', Listar.as_view(), name='listar'),
    path('bonos/descargar', Descargar.as_view(), name='descargar'),
    path('bonos/cargar-excel', CargarExcel.as_view(), name='cargar'),
    path('bonos/editar/<uuid:uuid>', Editar.as_view(), name='editar'),
    path('bonos/eliminar/<uuid:uuid>', Eliminar.as_view(), name='eliminar')
]