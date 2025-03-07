# Django
from django.db import models
from django.contrib.postgres.fields import JSONField
# utils
from utils.models import ControlInfo


class Bono(ControlInfo):
    class Meta:
        ordering = ('abonado__name', 'fecha_reg')
    identifier = 'OMB'
    tipos = (
        ('abonado', 'Abonado'),
        ('comprado', 'Comprado'),
        ('vitalicio', 'Vitalicio'),
        ('cortesia', 'Cortesía'),
        ('palco', 'Palco'),
        ('jaguares_palco', 'Palco Jaguares'),
        ('seguridad', 'Seguridad'),
        ('operativo', 'Operativo'),
        ('network', 'Network'),
        ('directiva', 'Directiva'),
        ('admin', 'Administración'),
        ('tarjeton', 'Tarjetón Est'),
        ('zona_comercial', 'Zona Comercial'),
        ('jaguares_cabecera_norte', 'Cabecera Norte Jaguares'),
        ('jaguares_cabecera_sur', 'Cabecera Sur Jaguares'),
        ('jaguares_preferente', 'Preferentes Jaguares'),
        ('jaguares_sombra', 'Sombra Jaguares'),
        ('napoli', 'Napolibono'),
    )
    tipo = models.CharField(choices=tipos, max_length=100, default='cortesia')
    abonado = JSONField(editable=False) #(nombre, teléfono, correo opcional)
    ubicacion = JSONField(editable=False) #(sección, fila, no. butaca)
    pago = JSONField(editable=False, null=True) #(tipo, a quién, monto)


class Partidos(ControlInfo):
    identifier = 'PTD'
    nombre = models.CharField(max_length=100)
    fecha = models.DateField(null=True)
    hora = models.TimeField(null=True)
    lugar = models.CharField(max_length=100, choices=(('centenario', 'Estadio Centenario 27 de Febrero'),))


class Asistencias(ControlInfo):
    identifier = 'ASIS'
    total_lecturas = models.SmallIntegerField(default=0)
    partido = models.ForeignKey(Partidos, on_delete=models.PROTECT, related_name='asistencias_partido')
    bono = models.ForeignKey(Bono, on_delete=models.PROTECT, related_name='bonos_partido')