# Django
from django.db import models
from django.contrib.postgres.fields import JSONField
# utils
from utils.models import ControlInfo

class Bono(ControlInfo):
    identifier = 'OMB'
    tipos = (
        ('abonado', 'Abonado'),
        ('comprado', 'Comprado'),
        ('vitalicio', 'Vitalicio'),
        ('cortesia', 'Cortesía'),
        ('palco', 'Palco'),
        ('seguridad', 'Seguridad'),
        ('operativo', 'Operativo'),
        ('network', 'Network'),
        ('directiva', 'Directiva'),
        ('admin', 'Administración'),
        ('tarjeton', 'Tarjetón Est')
    )
    tipo = models.CharField(choices=tipos, max_length=10, default='cortesia')
    abonado = JSONField(editable=False) #(nombre, teléfono, correo opcional)
    ubicacion = JSONField(editable=False) #(sección, fila, no. butaca)