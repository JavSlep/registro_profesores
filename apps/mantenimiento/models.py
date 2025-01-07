import uuid
from django.db import models
from ..establecimiento.models import Establecimiento
from ..usuario.models import Entidad

class MontoMantenimiento(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36) 
    establecimiento=models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
    year = models.IntegerField(null=True, blank=True)
    monto = models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)    
    class Meta:
        verbose_name="monto mantenimiento"
        verbose_name_plural="monto mantenimiento"
    def __str__(self):
        return self.establecimiento.nombre

class NominaPrecios(models.Model):               
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)    
    codigo = models.CharField(max_length=100) 
    nombre = models.CharField(max_length=200, null=True, blank=True )
    observacion = models.TextField(null=True, blank=True)
    proveedor = models.ForeignKey(Entidad, on_delete=models.PROTECT, null=True, blank=True)
    year = models.IntegerField(default=2024)
    class Meta:
        verbose_name="nomina precio"
        verbose_name_plural="nominas de precios"  
    
    def __str__(self):       
        return self.codigo

class CategoriaPartidas(models.Model):          
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)    
    nombre = models.CharField(max_length=300)
    nomina_precios = models.ForeignKey(NominaPrecios, on_delete=models.CASCADE, null=True, blank=True)    
    class Meta:
        verbose_name="categoria"
        verbose_name_plural="categorias"
    def __str__(self):
        return self.nombre

class PartidaNomina(models.Model):          
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    codigo = models.IntegerField()
    nomina_precios = models.ForeignKey(NominaPrecios, on_delete=models.PROTECT, null=True, blank=True)
    precio = models.IntegerField()
    unidad = models.CharField(max_length=36)    
    nombre = models.CharField(max_length=300)
    categoria = models.ForeignKey(CategoriaPartidas, on_delete=models.PROTECT, null=True, blank=True)    
    class Meta:
        verbose_name="partida"
        verbose_name_plural="partidas"
    def __str__(self):
        string = 'Cód:' + str(self.codigo) + ' | ' + self.nombre + ' | ' + self.unidad + ' | $ ' + str(self.precio)  
        return string
    
      