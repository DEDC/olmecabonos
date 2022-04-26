# Django
from django.db import models
from django.contrib.postgres.fields import JSONField
# utils
from utils.models import ControlInfo

class Bono(ControlInfo):
    identifier = 'OMB'
    tipos = (
        ('comprado', 'Comprado'),
        ('vitalicio', 'Vitalicio'),
        ('cortesia', 'Cortesía'),
        ('palco', 'Palco')
    )
    tipo = models.CharField(choices=tipos, max_length=10, default='cortesia')
    abonado = JSONField() #(nombre, teléfono, correo opcional)
    ubicacion = JSONField() #(sección, fila, no. butaca)