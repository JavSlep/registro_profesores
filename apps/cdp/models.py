from django.db import models
from django.utils import timezone
from babel.numbers import format_decimal
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..establecimiento.models import Establecimiento
from ..usuario.models import Unidad


class Year(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    year = models.IntegerField(default=2021)
    pdf_programa_presupuestario = models.FileField(upload_to='pdfs/', null=True, blank=True)


    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    
    @property
    def monto_total_ley_presupuestaria(self):

        return sum(subtitulo.ley_presupuestaria_subtitulo for subtitulo in self.subtitulos_presupuestarios.all())
    @property
    def monto_total_comprometido(self):
        return sum(subtitulo.monto_comprometido_subtitulo for subtitulo in self.subtitulos_presupuestarios.all())
    
    def __str__(self):
        return (
            f"Year: {self.year}, "
            f"Monto total ley presupuestaria: {self.monto_total_ley_presupuestaria}, "
            f"Monto total comprometido: {self.monto_total_comprometido}"
        )


class Subtitulo(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)

    n_subtitulo = models.CharField(max_length=2, default="")
    denominacion = models.CharField(max_length=50)

    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Subtitulo: "+self.n_subtitulo+", Denominacion: "+self.denominacion

PROGRAMAS_PRESUPUESTARIOS = [
    ('P01 GASTOS ADMINISTRATIVOS', 'P01 GASTOS ADMINISTRATIVOS'),
    ('P02 SERVICIOS EDUCATIVOS', 'P02 SERVICIOS EDUCATIVOS'),
]
class SubtituloPresupuestario(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    
    programa_presupuestario = models.CharField(max_length=50, choices=PROGRAMAS_PRESUPUESTARIOS)
    #Relaciones
    subtitulo = models.ForeignKey(Subtitulo, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='subtitulos_presupuestarios' ,null=True, blank=True)
    #################################################################

    ley_presupuestaria_subtitulo = models.IntegerField(null=False,default=0)#Este es un valor de la ley de presupuesto
    #Tambien hay un atributo oculto llamado items_presupuestarios
    
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)

    @property
    def concepto_presupuestario(self):
        return f"{self.subtitulo.n_subtitulo} {self.subtitulo.denominacion}"
    @property #Suma el monto comprometido más los cdps de todos los items presupuestarios
    def monto_comprometido_subtitulo(self):
        return sum(item.saldo_comprometido for item in self.items_presupuestarios.all())
    
    @property
    def monto_ejecucion_presupuestaria_subtitulo(self):
        return sum(item.ejecucion_presupuestaria_item for item in self.items_presupuestarios.all())

    @property #Saldo total por comprometer
    def monto_por_comprometer(self):
        return self.ley_presupuestaria_subtitulo - self.monto_comprometido_subtitulo

    def formatear_monto(self, monto):
        return format_decimal(monto, locale='es_ES')

    def __str__(self):
        return (
            f"Programa: {self.programa_presupuestario}, "
            f"{self.subtitulo.n_subtitulo} {self.subtitulo.denominacion}, "
            f"Ley presupuestaria: {self.formatear_monto(self.ley_presupuestaria_subtitulo)}, "
            f"Monto comprometido: {self.formatear_monto(self.monto_comprometido_subtitulo)}"
        )


class Item(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)

    n_item = models.CharField(max_length=2, default="")
    denominacion = models.CharField(max_length=50)
    subtitulo = models.ForeignKey(Subtitulo, on_delete=models.CASCADE)

    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subtitulo.n_subtitulo+", item: "+self.n_item+", Denominacion: "+self.denominacion


class ItemPresupuestario(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)

    subtitulo_presupuestario = models.ForeignKey(SubtituloPresupuestario, on_delete=models.CASCADE,related_name='items_presupuestarios',default=99)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ley_presupuestaria_item = models.IntegerField(null=False,default=0)#Este es un valor de la ley de presupuesto
    ejecucion_presupuestaria_item = models.IntegerField(default=0)
    monto_comprometido = models.IntegerField(null=False,default=0)

    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    
    @property
    def concepto_presupuestario_item(self):
        return self.item.subtitulo.n_subtitulo+self.item.n_item+" "+self.item.denominacion
    
    @property
    def saldo_comprometido(self):
        monto_total = sum(cdp.monto for cdp in self.cdps.all())+self.monto_comprometido
        return monto_total
    
    def formatear_monto(self, monto):
        return format_decimal(monto, locale='es_ES')
    
    #signals para guardar el monto comprometido en el subtitulo presupuestario

    def __str__(self):
        return(
            f"Programa: {self.subtitulo_presupuestario.programa_presupuestario}, "
            f"concepto presupuestario: {self.concepto_presupuestario_item}, "
            f"Ley presupuestaria: {self.formatear_monto(self.ley_presupuestaria_item)}, "
            f"Saldo comprometido: {self.formatear_monto(self.saldo_comprometido)}"
        )

NIVELS = [
    ('1', 'Nivel 1'),
    ('2', 'Nivel 2'),
    ('3', 'Nivel 3'),
]

class EjecucionPresupuestaria(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)

    nivel = models.CharField(max_length=1, choices=NIVELS)
    subtitulo_presupuestario = models.ForeignKey(SubtituloPresupuestario, on_delete=models.CASCADE, null=True, blank=True)
    item_presupuestario = models.ForeignKey(ItemPresupuestario, on_delete=models.CASCADE, null=True, blank=True)

    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)

#Relacionar ejecucion presupuetaria y sumar los montos totales
    @property
    def saldo_por_comprometer(self):
        if self.subtitulo_presupuestario:#Si el subtitulo presupuestario esta definido
            monto_ley_presupuesto = self.subtitulo_presupuestario.ley_presupuestaria_subtitulo
            monto_comprometido = self.subtitulo_presupuestario.monto_comprometido_subtitulo

            return monto_ley_presupuesto - monto_comprometido
        if self.item_presupuestario:
            monto_ley_presupuesto = self.item_presupuestario.ley_presupuestaria_item
            monto_comprometido = self.item_presupuestario.monto_comprometido
            return monto_ley_presupuesto - monto_comprometido
    


    @property
    def ejecucion_comprometida(self):#Porcentaje entre el valor comprometido y el total de la ley de presupuesto
        if self.subtitulo_presupuestario:
            return round((self.subtitulo_presupuestario.monto_comprometido_subtitulo / self.subtitulo_presupuestario.ley_presupuestaria_subtitulo) * 100)
        if self.item_presupuestario:
            return round((self.item_presupuestario.monto_comprometido / self.item_presupuestario.ley_presupuestaria_item) * 100)
    
    @property
    def nivel_cruce(self):
        if self.subtitulo_presupuestario:
            return 1
        if self.item_presupuestario:
            return 2

    def __str__(self):
        if self.subtitulo_presupuestario:
            return f"Nivel de cruce: {self.nivel_cruce}, Subtitulo: {self.subtitulo_presupuestario.subtitulo.denominacion}, Ley presupuestaria: {self.subtitulo_presupuestario.ley_presupuestaria_subtitulo}, Monto comprometido: {self.subtitulo_presupuestario.monto_comprometido_subtitulo}"
        if self.item_presupuestario:
            return f"Nivel de cruce: {self.nivel_cruce}, Item: {self.item_presupuestario.item.denominacion}, Ley presupuestaria: {self.item_presupuestario.ley_presupuestaria_item}, Monto comprometido: {self.item_presupuestario.monto_comprometido}"


#############--------------------------------------Cdp--------------------------################

class CdpCounter(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.count)


FONDOS = [
    ('SEP', 'SEP'),
    ('NORMAL/REGULAR', 'NORMAL/REGULAR'),
    ('PIE', 'PIE'),
    ('JUNJI', 'JUNJI'),
    ('PRO-RETENCION', 'PRO-RETENCION'),
    ('MANTENIMIENTO', 'MANTENIMIENTO'),
    ('APORTE FISCAL', 'APORTE FISCAL'),
    ('OTROS','OTROS')
]
# Create your models here.
class Cdp(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
     
    #Relaciones
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE,null=True, blank=True)
    unidad = models.ForeignKey(Unidad, on_delete=models.PROTECT,null=True, blank=True)
    item_presupuestario = models.ForeignKey(ItemPresupuestario, on_delete=models.CASCADE, related_name='cdps',null=False, blank=False)
    ##########################################################
    #El programa se saca del item presupuestario
    ##########################################################
    numero_requerimiento = models.IntegerField()
    fondo = models.CharField(max_length=20, choices=FONDOS)
    # cuenta_contable = models.CharField(max_length=50) Este dato se puede sacar de la tabla de items 2102
    cdp = models.CharField(max_length=4,blank=True,editable=False)
    folio_sigfe = models.CharField(max_length=5)
    n_orden = models.CharField(max_length=50)
    monto = models.IntegerField()
    detalle = models.CharField(max_length=500)
    otros = models.CharField(max_length=100, blank=True, null=True)

    fecha_cdp = models.DateField(default=timezone.now)
    fecha_guia_requerimiento = models.DateField()
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.cdp:
            counter, created = CdpCounter.objects.get_or_create(id=1)
            counter.count += 1
            counter.save()
            self.cdp = f"{counter.count}" 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"CDP:{self.cdp} ,{self.item_presupuestario.subtitulo_presupuestario.programa_presupuestario}, {self.item_presupuestario.subtitulo_presupuestario.concepto_presupuestario}, cuenta: {self.item_presupuestario.item.denominacion} monto_cdp: {self.monto}"


    
class Files(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    nombre = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(upload_to='pdfs/')
    id_relacion = models.CharField(max_length=36)
    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nombre

#---------------------|Signals|---------------------  
# Signal para resetear el contador 
@receiver(post_save, sender=Year)
def reset_cdp_counter(sender, instance, created, **kwargs):
    if created:#Creado por primera vez (true) o actualizacion (false)
        CdpCounter.objects.all().delete()
        CdpCounter.objects.create(id=1)

