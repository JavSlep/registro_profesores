from django.db import models
import uuid
from ..establecimiento.models import Establecimiento
from .models import FONDOS, Year

class ProyeccionAnual(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    #-------------------------Relacion-------------------------#
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='proyeccion')
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE, related_name='proyeccion')
    #subvenciones
    #----------------------------------------------------------#

    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.year.year} - {self.establecimiento.nombre}"
class Subvencion(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    #-------------------------Relacion-------------------------#
    proyeccion_anual = models.ForeignKey(ProyeccionAnual, on_delete=models.CASCADE,related_name='subvenciones')
    fondo = models.CharField(max_length=20, choices=FONDOS)
    #meses_proyectados
    #----------------------------------------------------------#

    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.fondo} - {self.proyeccion_anual.year.year}"

ESTADOS_MONTO = [
    ('Estimado', 'Estimado'),
    ('Real', 'Real'),
]
MESES = [
    (1, 'Enero'),
    (2, 'Febrero'),
    (3, 'Marzo'),
    (4, 'Abril'),
    (5, 'Mayo'),
    (6, 'Junio'),
    (7, 'Julio'),
    (8, 'Agosto'),
    (9, 'Septiembre'),
    (10, 'Octubre'),
    (11, 'Noviembre'),
    (12, 'Diciembre')
]
class MesProyectado(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    #-------------------------Relacion-------------------------#
    subvencion = models.ForeignKey(Subvencion, on_delete=models.CASCADE,related_name='meses_proyectados')
    mes = models.CharField(max_length=20, choices=MESES)
    monto = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS_MONTO, null=False, blank=False)
    #----------------------------------------------------------#

    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    
    @property
    def nombre_establecimiento(self):
        return self.subvencion.proyeccion_anual.establecimiento.nombre
    def __str__(self):
        return f"{self.mes} - {self.subvencion.fondo} - {self.subvencion.proyeccion_anual.year.year} - {self.monto} - {self.estado}"