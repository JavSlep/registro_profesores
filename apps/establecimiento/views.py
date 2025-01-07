from django.shortcuts import render  
from ..mantenimiento.models import MontoMantenimiento
from .models import *
from datetime import datetime
from django.utils.timezone import now


def listadoEstablecimientos(request):
    establecimientos = Establecimiento.objects.all()
    contexto = {
        'establecimientos':establecimientos
    }
    return render(request, 'establecimiento/listado_establecimientos.html', contexto)


def detalleEstablecimiento(request, id_establecimiento):    
    establecimiento =  Establecimiento.objects.get(id=id_establecimiento)    
    contexto = {
        'title_nav': 'Establecimientos',
        'establecimiento':establecimiento,        
    }
    return render(request, 'establecimiento/detalle_establecimiento.html', contexto)

from django.utils.timezone import make_aware
from django.utils.timezone import get_current_timezone

def escritorioEstablecimiento(request, id_establecimiento):
    establecimiento =  Establecimiento.objects.get(id=id_establecimiento)
    plan = PlanInfraestructura.objects.filter(establecimiento=id_establecimiento, year=2025).first()
    diagnostico = Diagnostico.objects.filter(establecimiento=id_establecimiento, year=2025).first()
    dias_restantes = None
    if plan and plan.estado == 1:    
        fecha_actual = now()        
        fecha_naive = datetime(2024, 12, 20, 0, 0, 0)
        fecha_fija = make_aware(fecha_naive, timezone=get_current_timezone())
        dias_restantes = fecha_fija - fecha_actual
        dias_restantes = dias_restantes.days        
    contexto = {
        'dias_restantes':dias_restantes,
        'plan':plan,
        'diagnostico':diagnostico,
        'establecimiento':establecimiento,
        'title_nav': 'Establecimiento',    
    }
    return render(request, 'establecimiento/escritorio_establecimiento.html', contexto)
    