import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from ..general.models import Comuna, Region
from ..establecimiento.models import Establecimiento

# Modelo Usuario
class User(AbstractUser):  
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    email = models.EmailField(unique=True)  
    username = models.CharField(max_length=60, null=True, blank=True)
    telefono = models.CharField(max_length=60, null=True, blank=True)
    cargo = models.CharField(max_length=80, null=True, blank=True)
    
    
    
    iniciales=models.CharField(max_length=3, null=True, blank=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    rut=models.CharField(max_length=12, unique=True, null=True, blank=True)  
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)  

    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['username']
        
    class Meta:
        verbose_name="usuario"
        verbose_name_plural="usuarios"
        
    def __str__(self):
        return '%s %s' %(self.first_name, self.last_name)
    
    @property
    def nombre_completo(self):    
        return '%s %s' %(self.first_name, self.last_name)
    
    def save(self,*args, **kwargs):    
        if not(self.iniciales) and self.first_name and self.last_name:
            self.iniciales = self.first_name[0].upper() + self.last_name[0].upper()
        super(User,self).save(*args, **kwargs)

# Modelo Entidad
tipo_entidad = [
  (1,'SLEP'),
  (2,'Externo'),
]
class Entidad(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)   
    nombre=models.CharField(max_length=100)
    rut=models.CharField(max_length=12, null=True, blank=True)  
    direccion=models.CharField(max_length=100)
    comuna=models.ForeignKey(Comuna, on_delete=models.PROTECT)
    region=models.ForeignKey(Region, on_delete=models.PROTECT)
    giro = models.CharField(max_length=300, null=True, blank=True)
    contacto = models.CharField(max_length=300, null=True, blank=True)
    telefono=models.CharField(max_length=12, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)     
    tipo_entidad=models.IntegerField(default=1, choices=tipo_entidad)   
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)  
    class Meta:
        verbose_name="entidad"
        verbose_name_plural="entidades"
    def __str__(self):
        return self.nombre

class Unidad(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    nombre=models.CharField(max_length=100)
    
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)    
    class Meta:
        verbose_name="unidad"
        verbose_name_plural="unidades" 
    def __str__(self):
        return f'{self.nombre}'


class AreaUnidad(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    #Relaciones entre entidades
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    ########################################
    nombre = models.CharField(max_length=100)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)


class UsuarioEntidad(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    #Relaciones entre entidades
    usuario=models.ForeignKey(User, on_delete=models.PROTECT)
    entidad=models.ForeignKey(Entidad, on_delete=models.PROTECT)
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.PROTECT,null=True, blank=True)
    area_unidad = models.ForeignKey(AreaUnidad, on_delete=models.PROTECT, null=True, blank=True)
    ########################################
    cargo=models.CharField(max_length=200, null=True, blank=True)
    """ departamento_unidad = models.ForeignKey(Establecimiento, on_delete=models.PROTECT,null=True, blank=True) """
    administrador = models.BooleanField(default=False, null=True, blank=True)
    estado=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        verbose_name="usuario entidad"
        verbose_name_plural="usuarios entidad" 
    def __str__(self):
        return '%s | Entidad: %s' %(self.usuario.nombre_completo, self.entidad)

