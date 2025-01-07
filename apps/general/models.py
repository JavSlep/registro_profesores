import os
import uuid
from django.db import models
from datetime import date

# Modelo Región
class Region(models.Model):  
  nombre=models.CharField(max_length=50, verbose_name="Región")
  class Meta:
    verbose_name="region"
    verbose_name_plural="regiones"
  def __str__(self):
    return self.nombre
  
# Modelo Comuna
class Comuna(models.Model):  
    nombre=models.CharField(max_length=50, verbose_name="Comuna")
    region=models.ForeignKey(Region, on_delete=models.CASCADE)  
    class Meta:
      verbose_name="comuna"
      verbose_name_plural="comunas"
    def __str__(self):
      return self.nombre



