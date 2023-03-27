# Djanfo
from django.urls import path
from apps.bonos.views import Registrar, Listar, Descargar

urlpatterns = [
    path('', Registrar.as_view(), name='registro'),
    path('bonos', Listar.as_view(), name='listar'),
    path('bonos/descargar', Descargar.as_view(), name='descargar')
]