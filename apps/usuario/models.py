import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser



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



