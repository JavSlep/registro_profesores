import uuid
from django.db import models
from ..general.models import Region, Comuna
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
import datetime
import os

#ok
class Item(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    codigo=models.CharField(max_length=50)
    nombre=models.CharField(max_length=200)    
    descripcion = models.TextField(null=True, blank=True)    
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)    
    class Meta:
        verbose_name="Items"
        verbose_name_plural="Items"
    def __str__(self):
        return self.nombre

class CategoriaPartida(models.Model):
    codigo=models.CharField(max_length=50, null=True, blank=True)    
    nombre=models.CharField(max_length=200, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)    
    class Meta:
        verbose_name="Categoría Partida"
        verbose_name_plural="Categorías Partidas"
    def __str__(self):
        return self.nombre
    
#ok

class TipoUnidad(models.Model):   
    nombre=models.CharField(max_length=200)   
    class Meta:
        verbose_name="Tipo Unidad"
        verbose_name_plural="Tipos de unidad"
    def __str__(self):
        return self.nombre


class Partida(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    codigo=models.CharField(max_length=50, null=True, blank=True, verbose_name="Código")
    precio = models.IntegerField(null=True, blank=True, default=0)
    categoria_partida=models.ForeignKey(CategoriaPartida, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Categoría")
    nombre=models.CharField(max_length=200, null=True, blank=True)
    unidad = models.ForeignKey(TipoUnidad,on_delete=models.PROTECT)
    descripcion = models.TextField(null=True, blank=True, verbose_name="Descripción")    
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)    
    class Meta:
        verbose_name="Partida"
        verbose_name_plural="Partidas"
    def __str__(self):
        return self.nombre
    
    """ def save(self,*args, **kwargs):
        if self.partida_nomina and not(self.nombre):
            self.nombre = self.partida_nomina.nombre         
        if self.partida_nomina and not(self.precio):
            self.precio = self.partida_nomina.precio
        if not(self.codigo) and self.partida_nomina:
            self.codigo = self.partida_nomina.codigo        
        super(Partida,self).save(*args, **kwargs) """

#ok
class Partida_PartidaMantencion(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    cantidad = models.IntegerField(default=0, null=True, blank=True)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    partida_mantencion = models.ForeignKey('mantenimiento.PartidaNomina', on_delete=models.PROTECT, null=True, blank=True, verbose_name="Partida Asociada (Nómina de Precios Mantención)")
    class Meta:
            verbose_name="Partida - Partida Mantención"
            verbose_name_plural="Partidas - Partidas Mantención"
    def __str__(self):
        return self.partida.nombre + '-' + self.partida_mantencion.nombre
    @property
    def total(self):
        total = self.cantidad * self.partida_mantencion.precio
        return total
    
@receiver(post_save, sender=Partida_PartidaMantencion)
def actualizaPrecioPartida_add(sender, instance, **kwargs):
    id_partida = instance.partida.id
    partida = Partida.objects.get(id=id_partida)
    total_partida = 0
    listado_partida_partidaMantencion = Partida_PartidaMantencion.objects.filter(partida=id_partida)    
    for partida_mantencion in listado_partida_partidaMantencion:
        total_partida += partida_mantencion.total
    partida.precio = total_partida
    partida.save()
      
@receiver(post_delete, sender=Partida_PartidaMantencion)
def actualizaPrecioPartida_delete(sender, instance, **kwargs):
    id_partida = instance.partida.id
    partida = Partida.objects.get(id=id_partida)
    total_partida = 0
    listado_partida_partidaMantencion = Partida_PartidaMantencion.objects.filter(partida=id_partida)
    if listado_partida_partidaMantencion:
        for partida_mantencion in listado_partida_partidaMantencion:
            total_partida += partida_mantencion.total
        partida.precio = total_partida
    else:
        partida.precio = 0
    partida.save()



  
#ok
class Item_Partida(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    class Meta:
            verbose_name="Item Partida"
            verbose_name_plural="Items Partidas"
    def __str__(self):
        return self.item.nombre + '-' + self.partida.nombre 

#ok
class CategoriaRecinto(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    codigo=models.CharField(max_length=50)
    nombre=models.CharField(max_length=200)    
    descripcion = models.TextField(null=True, blank=True)
    boolean_pabellon = models.BooleanField(default=True, null=True, blank=True)
    boolean_area = models.BooleanField(default=False, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)    
    class Meta:
        verbose_name="Categoría Recintos"
        verbose_name_plural="Categorías de Recintos"
    def __str__(self):
        return self.nombre
    
class CategoriaInstalaciones(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    codigo=models.CharField(max_length=50)
    nombre=models.CharField(max_length=200)   
    descripcion = models.TextField(null=True, blank=True)
    icono = models.CharField(max_length=200, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)    
    class Meta:
        verbose_name="Categoría Instalaciones"
        verbose_name_plural="Categorías Instalaciones"
    def __str__(self):
        return self.nombre

#ok
class TipoRecinto(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    codigo=models.CharField(max_length=50)
    nombre=models.CharField(max_length=200)    
    descripcion = models.TextField(null=True, blank=True)
    categoria=models.ForeignKey(CategoriaRecinto, on_delete=models.PROTECT, null=True, blank=True)
    categoria_instalaciones = models.ManyToManyField(CategoriaInstalaciones, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)    
    class Meta:
        verbose_name="Tipo Recinto"
        verbose_name_plural="Tipos de Recinto"
    def __str__(self):
        return self.nombre

#ok
class TipoRecinto_Item(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    tipo_recinto = models.ForeignKey(TipoRecinto, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    class Meta:
            verbose_name="Item Partida"
            verbose_name_plural="Items Partidas"
    def __str__(self):
        return self.tipo_recinto.nombre + '-' + self.item.nombre 
 
class CategoriaEstablecimiento(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)   
    nombre=models.CharField(max_length=100)
    class Meta:
        verbose_name="categoría establecimiento"
        verbose_name_plural="categorías de establecimientos"
    def __str__(self):
        return self.nombre

listado_area_geografica = [
    (1,'Urbano'),
    (2,'Rural'),    
]

estado_establecimiento = [
    (1,'Activo'),
    (2,'Inactivo'),
    
]

class Establecimiento(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)   
    codigo=models.CharField(max_length=50)
    digito = models.CharField(max_length=1, null=True, blank=True)
    letra_numero=models.CharField(max_length=50, null=True, blank=True)
    nombre=models.CharField(max_length=100)
    estado = models.IntegerField(default=1, choices=estado_establecimiento)   
    categoria=models.ForeignKey(CategoriaEstablecimiento, on_delete=models.PROTECT)
    region=models.ForeignKey(Region, on_delete=models.PROTECT)
    comuna=models.ForeignKey(Comuna, on_delete=models.PROTECT)    
    direccion=models.CharField(max_length=100)
    zona_geografica = models.IntegerField(default=1, choices=listado_area_geografica)
    director = models.CharField(max_length=100, null=True, blank=True)
    telefono1 = models.CharField(max_length=50, null=True, blank=True)
    telefono2 = models.CharField(max_length=50, null=True, blank=True)    
    email_establecimiento = models.EmailField(null=True, blank=True)
    email_director = models.EmailField(null=True, blank=True)    
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)    
    class Meta:
        verbose_name="establecimiento"
        verbose_name_plural="establecimientos"
    def __str__(self):
        return self.nombre

    @property
    def rbd(self):
        if self.digito:
            rbd = self.codigo + "-" + self.digito
        else:
            rbd = self.codigo    
        return rbd
    
    @property
    def matricula_actual(self):
        current_date = datetime.date.today()    
        year =  current_date.year        
        matricula_actual = Matricula.objects.filter(year=year, establecimiento=self.id).first()              
        return matricula_actual
   
class Matricula(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36) 
    establecimiento=models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
    year = models.IntegerField(null=True, blank=True)
    matricula = models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)    
    class Meta:
        verbose_name="matricula"
        verbose_name_plural="matriculas"
    def __str__(self):
        matricula = str(self.matricula)
        return matricula


estado_plan_infra = [
    (1, 'Borrador'),    
    (2, 'Enviado'),
    (3, 'Observado'),
    (4, 'Aprobado'),
    (5, 'Eliminado'),          
] 

class PlanInfraestructura(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36) 
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)    
    nombre=models.CharField(max_length=200, null=True, blank=True)
    estado = models.IntegerField(choices=estado_plan_infra, default=1)
    year = models.IntegerField(default=2024)
    descripcion = models.TextField(null=True, blank=True)
    fecha_envio=models.DateTimeField(null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)  
    class Meta:
        verbose_name="Plan Infraestructura"
        verbose_name_plural="Planes Infraestructura"
    def __str__(self):        
        return self.nombre
    
    @property
    def total(self):
        listado_pabellones = Pabellon.objects.filter(establecimiento=self.establecimiento.id)
        total = 0
        if  listado_pabellones: 
            for pabellon in listado_pabellones:
                total += pabellon.total
        return total

class MaterialidadPabellon(models.Model):    
    nombre=models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    class Meta:
        verbose_name="materialidad pabellon"
        verbose_name_plural="materialidades pabellones"
    def __str__(self):        
        return self.nombre
   
numero_pisos = [
    (1, '1 Piso'),    
    (2, '2 Pisos'),
    (3, '3 Pisos'),
    (4, '4 Pisos'),
    (5, '5 Pisos'),          
] 


tipo_pabellon = [
    (1, 'Edificacción'),    
    (2, 'Area Exterior'),             
] 

class Pabellon(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    codigo=models.CharField(max_length=50, null=True, blank=True)
    tipo_pabellon = models.IntegerField(choices=tipo_pabellon, default=1, null=True, blank=True)
    nombre=models.CharField(max_length=200)
    numero_pisos = models.IntegerField(choices=numero_pisos, default=1)
    descripcion = models.TextField(null=True, blank=True)    
    establecimiento=models.ForeignKey(Establecimiento, on_delete=models.CASCADE)    
    
    class Meta:
        verbose_name="pabellon"
        verbose_name_plural="pabellones"
    
    def __str__(self):        
        return self.nombre
    
    @property
    def total(self):
        listado_recinto = Recinto.objects.filter(pabellon=self.id)
        total = 0
        if  Recinto_Partida: 
            for recinto in listado_recinto:
                total += recinto.total
        return total
    
    
    @property
    def numero_recintos(self):
        numero_recintos = 0
        recintos = Recinto.objects.filter(pabellon=self.id)
        if recintos:
            numero_recintos = recintos.count()
        return numero_recintos
    @property
    def total_recintos_administrativos(self):
        return Recinto.objects.filter(pabellon=self.id, tipo_recinto__categoria__codigo = "RA").count()
    @property
    def total_recintos_docentes(self):
        return Recinto.objects.filter(pabellon=self.id, tipo_recinto__categoria__codigo = "RD").count()
        
class EstadoRecinto(models.Model):
    codigo = models.CharField(max_length=36)
    nombre = models.CharField(max_length=100)
    class_css = models.CharField(max_length=100, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    class Meta:
        verbose_name="Estado Recinto"
        verbose_name_plural="Estados Recinto"
    def __str__(self):        
        return self.nombre
  
class Recinto(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    nombre = models.CharField(max_length=36)
    estado = models.ForeignKey(EstadoRecinto, on_delete=models.PROTECT, default=1)
    observacion_estado = models.TextField(null=True, blank=True)
    piso = models.IntegerField(null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)    
    pabellon = models.ForeignKey(Pabellon, on_delete=models.CASCADE)
    tipo_recinto = models.ForeignKey(TipoRecinto, on_delete=models.PROTECT)    
    class Meta:
        verbose_name="Recinto pabellon"
        verbose_name_plural="Recinto pabellones"
    def __str__(self):        
        return self.nombre
    @property
    def total(self):
        listado_recinto_partida = Recinto_Partida.objects.filter(recinto=self.id)
        total = 0
        if  Recinto_Partida: 
            for partida in listado_recinto_partida:
                total += partida.total
        return total
    
# Signals
""" @receiver(post_save, sender=Recinto)
def creacionItemRecintoPabellon(sender, instance, **kwargs):    
    tipo_recinto = instance.tipo_recinto    
    lista_id_items_relacionados_tipo_recinto = list(tipo_recinto.tags_item.values_list('id', flat=True))
    items = Item.objects.filter(id__in=lista_id_items_relacionados_tipo_recinto)
    if items:
        for item in items:        
            ItemRecintoPabellon.objects.create(
                recinto_pabellon = instance,
                item = item,           
            ) """

class Recinto_Partida(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    plan = models.ForeignKey(PlanInfraestructura, on_delete=models.CASCADE, null=True, blank=True)    
    cantidad = models.IntegerField(default=0)    
    recinto = models.ForeignKey(Recinto, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE,null=True, blank=True )
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)    
    class Meta:
        verbose_name="Partida Recinto Pabellon"
        verbose_name_plural="Partidas Recinto Pabellones"
    def __str__(self):        
        return self.partida.nombre
    @property
    def total(self):
        total = self.cantidad * self.partida.precio        
        return total

class EstadoInstalaciones(models.Model):
    codigo = models.CharField(max_length=36)
    nombre = models.CharField(max_length=100)
    #background_color = models.CharField(max_length=100, null=True, blank=True)
    class_css = models.CharField(max_length=100, null=True, blank=True)   
    #text_color = models.CharField(max_length=100, null=True, blank=True)    
    descripcion = models.TextField(null=True, blank=True)
    class Meta:
        verbose_name="Estado Instalaciones"
        verbose_name_plural="Estados Instalaciones"
    def __str__(self):        
        return self.nombre

class Recinto_CategoriaInstalaciones(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)    
    estado = models.ForeignKey(EstadoInstalaciones, on_delete=models.CASCADE)
    plan = models.ForeignKey(PlanInfraestructura, on_delete=models.CASCADE, null=True, blank=True)
    recinto = models.ForeignKey(Recinto, on_delete=models.CASCADE)
    categoria_instalaciones = models.ForeignKey(CategoriaInstalaciones, on_delete=models.CASCADE)
    observaciones = models.TextField(null=True, blank=True)  
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        verbose_name="Instalación Recinto Pabellon"
        verbose_name_plural="Instalaciones Recinto Pabellones"
    def __str__(self):        
        return self.categoria_instalaciones.nombre
    
class Pabellon_CategoriaInstalaciones(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)    
    estado = models.ForeignKey(EstadoInstalaciones, on_delete=models.CASCADE)
    plan = models.ForeignKey(PlanInfraestructura, on_delete=models.CASCADE, null=True, blank=True)
    pabellon = models.ForeignKey(Pabellon, on_delete=models.CASCADE, null=True, blank=True)
    categoria_instalaciones = models.ForeignKey(CategoriaInstalaciones, on_delete=models.CASCADE)
    observaciones = models.TextField(null=True, blank=True)  
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        verbose_name="Instalación Pabellon"
        verbose_name_plural="Instalaciones Pabellones"
    def __str__(self):        
        return self.categoria_instalaciones.nombre
    
class Plan_CategoriaInstalaciones(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)    
    estado = models.ForeignKey(EstadoInstalaciones, on_delete=models.CASCADE)
    plan = models.ForeignKey(PlanInfraestructura, on_delete=models.CASCADE, null=True, blank=True)    
    categoria_instalaciones = models.ForeignKey(CategoriaInstalaciones, on_delete=models.CASCADE)
    observaciones = models.TextField(null=True, blank=True)  
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        verbose_name="Instalación Plan"
        verbose_name_plural="Instalaciones Plan"
    def __str__(self):        
        return self.categoria_instalaciones.nombre
  
    
    
# ***************************** Dignóstico ******************************************************
class Diagnostico(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36) 
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)    
    nombre=models.CharField(max_length=200, null=True, blank=True)
    estado = models.IntegerField(choices=estado_plan_infra, default=1)
    year = models.IntegerField(default=2024)
    descripcion = models.TextField(null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    fecha_envio=models.DateTimeField(null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)  
    class Meta:
        verbose_name="Diagnóstico"
        verbose_name_plural="Diagnóstico"
    def __str__(self):        
        return self.nombre
        
class Diagnostico_CategoriaInstalaciones(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)    
    estado = models.ForeignKey(EstadoInstalaciones, on_delete=models.CASCADE)
    diagnostico = models.ForeignKey(Diagnostico, on_delete=models.CASCADE, null=True, blank=True)    
    categoria_instalaciones = models.ForeignKey(CategoriaInstalaciones, on_delete=models.CASCADE)
    observaciones = models.TextField(null=True, blank=True)  
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        verbose_name="Diagnóstico - Instalaciones"
        verbose_name_plural="Diagnóstico - Instalaciones"
    def __str__(self):        
        return self.categoria_instalaciones.nombre

class TituloItemDiagnostico(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    nombre=models.CharField(max_length=200, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)   
    class Meta:
        verbose_name="Diagnóstico Título Item"
        verbose_name_plural="Diagnóstico Título Item"
    def __str__(self):        
        return self.nombre

class ItemDiagnostico(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    nombre=models.CharField(max_length=200)
    orden=models.IntegerField(null=True, blank=True)
    titulo_item = models.ForeignKey(TituloItemDiagnostico, on_delete=models.CASCADE, null=True, blank=True) 
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)    
    class Meta:
        verbose_name="Diagnóstico Item"
        verbose_name_plural="Diagnóstico Item"
    def __str__(self):
        return self.nombre
    
class PartidaDiagnostico(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    nombre=models.CharField(max_length=200)
    item = models.ForeignKey(ItemDiagnostico, on_delete=models.CASCADE, null=True, blank=True) 
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)    
    class Meta:
        verbose_name="Diagnóstico Partida"
        verbose_name_plural="Diagnóstico Partida"
    def __str__(self):
        return self.nombre

evaluacion = [
    (1, 'Sin evaluar'), 
    (2, 'No requiere mantención'),    
    (3, 'Requiere mantanción'),
    (4, 'No aplica'),             
] 

class Diagnostico_PartidaDiagnostico(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    diagnostico = models.ForeignKey(Diagnostico, on_delete=models.CASCADE) 
    partida_diagnostico = models.ForeignKey(PartidaDiagnostico, on_delete=models.CASCADE)
    evaluacion = models.IntegerField(choices=evaluacion, default=1, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    class Meta:
        verbose_name="Diagnóstico - Partida_Diagnóstico"
        verbose_name_plural="Diagnóstico - Partida_Diagnóstico"
    

def directorio_imagen_diagnostico(instance, filename):
    return 'diagnostico/{0}/{1}/img/{2}'.format(str(instance.diagnostico.year), instance.diagnostico.establecimiento.codigo, filename)

class ImagenDiagnostico(models.Model):  
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    diagnostico = models.ForeignKey(Diagnostico, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to=directorio_imagen_diagnostico, null=True, blank=True, max_length=300)
    created=models.DateTimeField(auto_now_add=True)  
    class Meta:
        verbose_name="Diagnóstico - Imagenes"
        verbose_name_plural="Diagnóstico - Imagenes"
    def __str__(self):
        return self.diagnostico.establecimiento.nombre 

# Signals imagen
@receiver(post_delete, sender=ImagenDiagnostico)
def eliminaArhivoImagenLocal(sender, instance, **kwargs):
    if instance.imagen:
        if os.path.isfile(instance.imagen.path):
            os.remove(instance.imagen.path)  