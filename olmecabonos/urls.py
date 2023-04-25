# Django
from django.urls import path
from apps.bonos.views import Registrar, Listar, Descargar, CargarExcel, Editar, Eliminar, Lector, Juegos, check_bonus

urlpatterns = [
    path('', Registrar.as_view(), name='registro'),
    path('bonos', Listar.as_view(), name='listar'),
    path('bonos/descargar', Descargar.as_view(), name='descargar'),
    path('bonos/cargar-excel', CargarExcel.as_view(), name='cargar'),
    path('bonos/editar/<uuid:uuid>', Editar.as_view(), name='editar'),
    path('bonos/eliminar/<uuid:uuid>', Eliminar.as_view(), name='eliminar'),
    path('bonos/<uuid:uuid>/lector', Lector.as_view(), name='lector'),
    path('bonos/juegos', Juegos.as_view(), name='juegos'),
    path('check/bonus', check_bonus, name='check_bonus')
]