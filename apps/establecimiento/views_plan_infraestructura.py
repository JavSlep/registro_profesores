from django.shortcuts import render, redirect
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from .models import *
from ..mantenimiento.models import PartidaNomina
import datetime
from django.contrib import messages
from .form import *
from ..mantenimiento.models import MontoMantenimiento
import random
    
def instruccionesPlanInfra(request, id_establecimiento):
    establecimiento = Establecimiento.objects.get(id=id_establecimiento)
    plan = PlanInfraestructura.objects.filter(establecimiento=id_establecimiento, year=2025).first()
    contexto = {
        'title_nav': 'Plan Infraestructura y Mantenimiento ' + str(2025),       
        'establecimiento':establecimiento,
        'plan':plan
    }
    return render(request, 'plan_infra/instrucciones_plan_infra.html', contexto)

def creacionInstalacionesPlan(id_plan):       
    plan = PlanInfraestructura.objects.get(id=id_plan)
    listado_instalaciones = CategoriaInstalaciones.objects.all()
    if listado_instalaciones:
        for i in listado_instalaciones:
            estado = EstadoInstalaciones.objects.filter(nombre="Sin Evaluar").first()        
            Plan_CategoriaInstalaciones.objects.create (
                estado = estado,
                plan = plan,
                categoria_instalaciones = i,                     
            )

def nuevoPlanInfra(request, id_establecimiento):
    establecimiento = Establecimiento.objects.get(id=id_establecimiento)    
    plan = PlanInfraestructura.objects.create (        
        establecimiento = establecimiento,   
        nombre= "Plan de Ingraestructura y Mantenimiento 2025",
        estado = 1,
        year = 2025,
        descripcion = 'Plan 2025'
    )
    creacionInstalacionesPlan(plan.id)
    messages.success(request, "Plan creado correctamente.")    
    return redirect('editar_plan_infra', plan.id, establecimiento.id)

def detallePlanInfra(request, id_plan, id_establecimiento):
    plan = PlanInfraestructura.objects.get(id=id_plan)
    establecimiento = Establecimiento.objects.get(id=id_establecimiento)
    listado_instalaciones = Plan_CategoriaInstalaciones.objects.filter(plan=plan) 
    contexto = {
        'title_nav': 'Plan Infraestructura y Mantenimiento ' + str(plan.year),        
        'establecimiento':establecimiento,
        'plan':plan,
        'listado_instalaciones':listado_instalaciones
    }
    return render(request, 'plan_infra/detalle_plan_infra.html', contexto)

def editarPlanInfra(request, id_plan, id_establecimiento):
    current_date = date.today()  
    year =  current_date.year
    plan = PlanInfraestructura.objects.get(id=id_plan)      
    establecimiento =  Establecimiento.objects.get(id=id_establecimiento)
    listado_pabellones =  Pabellon.objects.filter(establecimiento=id_establecimiento, tipo_pabellon = 1)
    listado_areas =  Pabellon.objects.filter(establecimiento=id_establecimiento, tipo_pabellon = 2)
    monto_mantenimiento_asignado =  MontoMantenimiento.objects.filter(establecimiento=id_establecimiento, year=2024).first() 
    if monto_mantenimiento_asignado:
        monto_mantenimiento_asignado = monto_mantenimiento_asignado.monto
    else:
        monto_mantenimiento_asignado = 0
    listado_instalaciones = Plan_CategoriaInstalaciones.objects.filter(plan=plan)
    cantidad_instalaciones_sin_evaluar = listado_instalaciones.count() - listado_instalaciones.exclude(estado__id=1).count()
    monto_saldo = monto_mantenimiento_asignado - plan.total
    contexto = {
        'title_nav': 'Plan Infraestructura y Mantenimiento ' + str(plan.year),
        'monto_mantenimiento_asignado':monto_mantenimiento_asignado,
        'monto_saldo':monto_saldo,      
        'establecimiento':establecimiento,
        'plan':plan,
        'listado_pabellones':listado_pabellones,
        'listado_areas':listado_areas,       
        'listado_instalaciones':listado_instalaciones,
        'cantidad_instalaciones_sin_evaluar':cantidad_instalaciones_sin_evaluar
    }
    return render(request, 'plan_infra/editar_plan_infra.html', contexto)

def detallePlanInfra(request, id_plan, id_establecimiento):
    plan = PlanInfraestructura.objects.get(id=id_plan)      
    establecimiento =  Establecimiento.objects.get(id=id_establecimiento)
    listado_pabellones =  Pabellon.objects.filter(establecimiento=id_establecimiento, tipo_pabellon = 1)
    listado_areas =  Pabellon.objects.filter(establecimiento=id_establecimiento, tipo_pabellon = 2)
    listado_instalaciones = Plan_CategoriaInstalaciones.objects.filter(plan=plan).exclude(estado__codigo='NE')
    cantidad_instalaciones_sin_evaluar = listado_instalaciones.filter(estado__codigo='S/E').count()    
    cantidad_instalaciones_sin_justificar = listado_instalaciones.filter(observaciones="").count()
    
    id_listado_pabellones = list(listado_pabellones.values_list('id', flat=True))
    id_listado_areas = list(listado_areas.values_list('id', flat=True))
    
    listado_recintos_pabellones = Recinto.objects.filter(pabellon__in=id_listado_pabellones)
    listado_recintos_areas = Recinto.objects.filter(pabellon__in=id_listado_areas)
    
    
    
    id_listado_recintos_pabellones = list(listado_recintos_pabellones.values_list('id', flat=True))    
    id_listado_recintos_areas = list(listado_recintos_areas.values_list('id', flat=True))
    
    listado_partidas_recinto_pabellones = Recinto_Partida.objects.filter(recinto__in = id_listado_recintos_pabellones).exclude(cantidad=0)    
    listado_partidas_recinto_areas = Recinto_Partida.objects.filter(recinto__in = id_listado_recintos_areas).exclude(cantidad=0)
    
     
       
    listado_id_item_recinto_pabellones = list(listado_partidas_recinto_pabellones.values_list('item', flat=True))
    listado_item_recinto_pabellones = Item.objects.filter(id__in=listado_id_item_recinto_pabellones)
    
    
    
    
    """ .order_by('item') """
    
    """ listado_instalaciones = Recinto_CategoriaInstalaciones.objects.filter(recinto = recinto, plan=plan) """
    
    contexto = {
        'title_nav': 'Plan Infraestructura y Mantenimiento ' + str(plan.year),
        'establecimiento':establecimiento,
        'plan':plan,
        'listado_pabellones':listado_pabellones,
        'listado_areas':listado_areas,
        'listado_instalaciones':listado_instalaciones,        
        'listado_recintos_pabellones':listado_recintos_pabellones,
        'listado_recintos_areas':listado_recintos_areas,
        'listado_partidas_recinto_pabellones':listado_partidas_recinto_pabellones,
        'listado_partidas_recinto_areas':listado_partidas_recinto_areas,        
        'listado_item_recinto_pabellones':listado_item_recinto_pabellones,        
        'cantidad_instalaciones_sin_evaluar':cantidad_instalaciones_sin_evaluar,
        'cantidad_instalaciones_sin_justificar':cantidad_instalaciones_sin_justificar
    }
    return render(request, 'plan_infra/detalle_plan_infra.html', contexto)
    
def creacionInstalacionesPabellon(id_pabellon, id_plan):
    pabellon = Pabellon.objects.get(id=id_pabellon)    
    plan = PlanInfraestructura.objects.get(id=id_plan)
    listado_instalaciones = CategoriaInstalaciones.objects.all()
    if listado_instalaciones:
        for i in listado_instalaciones:
            estado = EstadoInstalaciones.objects.filter(nombre="Sin Evaluar").first()        
            Pabellon_CategoriaInstalaciones.objects.create (
                estado = estado,
                plan = plan, 
                pabellon = pabellon,
                categoria_instalaciones = i,                     
            )

def nuevoPabellon(request, id_plan, id_establecimiento, tipo_pabellon):
    if tipo_pabellon == 1:
        form = PabellonForm()
    else:
        form = AreaExteriorForm()           
    establecimiento = Establecimiento.objects.get(id=id_establecimiento)    
    plan = PlanInfraestructura.objects.get(id=id_plan)   
    if request.method == 'POST':
        if tipo_pabellon == 1:
            form = PabellonForm(request.POST)
        else:
            form = AreaExteriorForm(request.POST)        
        if form.is_valid():
            pabellon = form.save()
            #creacionInstalacionesPabellon(pabellon.id, id_plan)
            messages.success(request, "Creado correctamente.")
            return redirect ('detalle_pabellon', id_plan, pabellon.id)    
    contexto = {
        'title_nav': 'Plan Infraestructura y Mantenimiento ' + str(plan.year),       
        'establecimiento':establecimiento,       
        'form': form,
        'plan':plan,
        'tipo_pabellon':tipo_pabellon        
    }
    return render(request, 'plan_infra/nuevo_pabellon.html', contexto)

def editarPabellon(request, id_plan, id_pabellon):
    pabellon = Pabellon.objects.get(id=id_pabellon)
    plan = PlanInfraestructura.objects.get(id=id_plan)  
    establecimiento = pabellon.establecimiento
    form = PabellonEditForm(instance=pabellon)    
    if request.method == 'POST':
        form = PabellonEditForm(request.POST, instance=pabellon)
        if form.is_valid():
            pabellon = form.save()         
            messages.success(request, "Editado correctamente.")
            return redirect ('detalle_pabellon', id_plan, pabellon.id)    
    contexto = {
        'title_nav': 'Plan Infraestructura y Mantenimiento ' + str(plan.year), 
        'establecimiento':establecimiento,
        'pabellon':pabellon,
        'plan':plan,
        'form': form,
    }
    return render(request, 'plan_infra/editar_pabellon.html', contexto)

def eliminarPabellon(request, id_plan, id_pabellon):
    pabellon = Pabellon.objects.get(id=id_pabellon)
    id_establecimiento = pabellon.establecimiento.id
    recintos_pabellon = Recinto.objects.filter(pabellon=pabellon)    
    if recintos_pabellon:
        messages.error(request, "Pabellón contiene recintos. No es posible eliminar.")
        return redirect('detalle_pabellon', id_plan,  id_pabellon)
    else:
        pabellon.delete()
        messages.success(request, "Pabellon eliminado correctamente.") 
        return redirect('editar_plan_infra', id_plan,  id_establecimiento)

def detallePabellon(request, id_plan, id_pabellon):
    plan = PlanInfraestructura.objects.get(id=id_plan)   
    pabellon = Pabellon.objects.get(id=id_pabellon)   
    recintos = Recinto.objects.filter(pabellon=id_pabellon)
    listado_instalaciones = Pabellon_CategoriaInstalaciones.objects.filter(plan=plan, pabellon=pabellon)
    pisos = []
    for piso in range(1, pabellon.numero_pisos + 1):
        recintos_en_piso = recintos.filter(piso=piso)
        listado_recintos = []
        for recinto in recintos_en_piso:
            listado_recintos.append(
                {
                    'piso': piso,
                    'id': recinto.id,
                    'nombre': recinto.nombre,
                    'descripcion': recinto.descripcion,                    
                    'tipo_recinto': recinto.tipo_recinto,
                    'total': recinto.total,
                    'estado': recinto.estado,                                    
                }
            )
        pisos.append(
            listado_recintos
        )  
    contexto = {
        'title_nav': 'Plan Infraestructura y Mantenimiento ' + str(plan.year),
        'plan':plan,
        'establecimiento':pabellon.establecimiento,
        'pabellon':pabellon,
        'pisos': pisos,        
        'listado_instalaciones':listado_instalaciones      
    }
    return render(request, 'plan_infra/detalle_pabellon.html', contexto)

def creacionPartidasRecinto(id_recinto, id_plan):
    recinto = Recinto.objects.get(id=id_recinto)
    plan = PlanInfraestructura.objects.get(id=id_plan)
    tipo_recinto = recinto.tipo_recinto
    # Obtención de todos los items relacionados con tipo de recinto.
    listado_tiporecinto_item = TipoRecinto_Item.objects.filter(tipo_recinto=tipo_recinto)    
    for i in listado_tiporecinto_item:        
        listado_item_partida = Item_Partida.objects.filter(item=i.item)
        for p in listado_item_partida:           
            Recinto_Partida.objects.create (
                plan = plan,   
                cantidad = 0,
                recinto = recinto,
                item = p.item,
                partida = p.partida
            )

def creacionInstalacionesRecinto(id_recinto, id_plan):
    recinto = Recinto.objects.get(id=id_recinto)
    plan = PlanInfraestructura.objects.get(id=id_plan)    
    tipo_recinto = recinto.tipo_recinto         
    for i in tipo_recinto.categoria_instalaciones.all():
        estado = EstadoInstalaciones.objects.filter(nombre="Sin Evaluar").first()        
        Recinto_CategoriaInstalaciones.objects.create (
            estado = estado,
            plan = plan, 
            recinto = recinto,
            categoria_instalaciones = i,                     
        )
      
def nuevoRecinto(request, id_plan, id_pabellon, piso):
    plan = PlanInfraestructura.objects.get(id=id_plan)
    form = RecintoForm()
    pabellon = Pabellon.objects.get(id=id_pabellon)
    tipo = pabellon.tipo_pabellon    
    if tipo == 1:
        listado_categoria_recinto = CategoriaRecinto.objects.filter(boolean_pabellon=True)
    else:
        listado_categoria_recinto = CategoriaRecinto.objects.filter(boolean_area=True)    
    listado_tipo_recinto = TipoRecinto.objects.all()    
    if request.method == 'POST':
        form = RecintoForm(request.POST)
        if form.is_valid():
            recinto = form.save()
            creacionPartidasRecinto(recinto.id, id_plan)
            #creacionInstalacionesRecinto(recinto.id, id_plan)
            messages.success(request, "Recinto creado correctamente.")
            return redirect ('detalle_pabellon', id_plan, id_pabellon)    
    contexto = {       
        'establecimiento': plan.establecimiento,
        'pabellon':pabellon,
        'piso':piso,
        'listado_categoria_recinto':listado_categoria_recinto,
        'listado_tipo_recinto':listado_tipo_recinto,
        'form':form,
        'plan':plan,
        'tipo':tipo
    }
    return render(request, 'plan_infra/nuevo_recinto.html', contexto)

def detalleRecinto(request, id_plan, id_recinto):
    plan = PlanInfraestructura.objects.get(id=id_plan)
    recinto = Recinto.objects.get(id=id_recinto)
    listado_partidas_recinto = Recinto_Partida.objects.filter(recinto = recinto).order_by('item')
    listado_id_item = list(listado_partidas_recinto.values_list('item', flat=True))
    listado_item = Item.objects.filter(id__in=listado_id_item)
    listado_instalaciones = Recinto_CategoriaInstalaciones.objects.filter(recinto = recinto, plan=plan)
    if recinto.estado.id != 1:
        boolean_estado = True
    else:
        boolean_estado = False   
    contexto = {
        'title_nav': 'Plan Infraestructura y Mantenimiento ' + str(plan.year),
        'establecimiento':recinto.pabellon.establecimiento,
        'plan':plan,        
        'pabellon':recinto.pabellon,
        'recinto':recinto,
        'listado_partidas_recinto':listado_partidas_recinto,
        'listado_item':listado_item,
        'listado_instalaciones':listado_instalaciones,
        'boolean_estado':boolean_estado              
    }
    return render(request, 'plan_infra/detalle_recinto.html', contexto)


def editarRecinto(request, id_plan, id_recinto):        
    recinto = Recinto.objects.get(id=id_recinto)
    plan = PlanInfraestructura.objects.get(id=id_plan) 
    form = EditRecintoForm(instance=recinto)      
    if request.method == 'POST':
        form = EditRecintoForm(request.POST, instance=recinto)
        if form.is_valid():
            recinto = form.save()         
            messages.success(request, "Editado correctamente.")
            return redirect ('detalle_recinto', id_plan, recinto.id)    
    contexto = {
        'title_nav': 'Plan Infraestructura y Mantenimiento ' + str(plan.year), 
        'recinto':recinto,
        'plan':plan,
        'form': form,
        'establecimiento':plan.establecimiento,
    }
    return render(request, 'plan_infra/editar_recinto.html', contexto)







def eliminarRecinto(request, id_plan, id_recinto):   
    recinto = Recinto.objects.get(id=id_recinto)
    id_pabellon = recinto.pabellon.id
    recinto.delete()
    messages.success(request, "Recinto eliminado correctamente.") 
    return redirect('detalle_pabellon', id_plan,  id_pabellon)

@csrf_exempt
def actualizaCantidadPartidaRencitoHtmx(request, id_recinto_partida):    
    recinto_partida = Recinto_Partida.objects.get(id = id_recinto_partida)
    if request.method == 'POST':                
        cantidad = request.POST['cantidad']
        if cantidad:
            cantidad=int(cantidad)
            if cantidad < 0:                
                messages.error(request, "La cantidad no puede ser negativa.")
                cantidad = recinto_partida.cantidad                 
            else:            
                recinto_partida.cantidad = cantidad
                recinto_partida.save()
                messages.success(request, "Cantidad actualizada correctamente.")     
        else:
            messages.error(request, "Debe ingresar una cantidad.")
            cantidad = recinto_partida.cantidad 
    contexto = {
        'id_recinto_partida': id_recinto_partida,
        'cantidad':cantidad,
        'total_recinto':recinto_partida.recinto.total,
        'total_partida':recinto_partida.total
    }
    return render(request, 'plan_infra/actualiza_cantidad_partida_recinto_htmx.html', contexto)

@csrf_exempt 
def actualizaInstalacionPabellonHtmx(request, id_instalacion):
    instalacion = Pabellon_CategoriaInstalaciones.objects.get(id = id_instalacion)
    form = Pabellon_CategoriaInstalacionesForm(instance=instalacion)
    if request.method == 'POST':        
        form = Pabellon_CategoriaInstalacionesForm(request.POST, instance=instalacion)
        if form.is_valid():
            instalacion = form.save()
            messages.success(request, "Instalación actualizada correctamente.")
            contexto = {       
                'instalacion':instalacion, 
            }
            return render(request, 'plan_infra/actualizaInstalacionPabellonHtmxPOST.html', contexto)
    contexto = {       
        'instalacion':instalacion,       
        'form': form,
    }
    return render(request, 'plan_infra/actualizaInstalacionPabellonHtmxGET.html', contexto)                

def actualizaInstalacionPabellonHtmxCancel(request, id_instalacion):
    instalacion = Pabellon_CategoriaInstalaciones.objects.get(id = id_instalacion)
    contexto = {       
        'instalacion':instalacion,
    }    
    return render(request, 'plan_infra/actualizaInstalacionPabellonHtmxPOST.html', contexto)

# *************** CRUD Instalaciones Plan ****************************
@csrf_exempt 
def actualizaInstalacionPlanHtmx(request, id_instalacion):    
    instalacion = Plan_CategoriaInstalaciones.objects.get(id = id_instalacion)    
    form = Plan_CategoriaInstalacionesForm(instance=instalacion)
    if request.method == 'POST':        
        form = Plan_CategoriaInstalacionesForm(request.POST, instance=instalacion)
        if form.is_valid():
            instalacion = form.save()
            listado_instalaciones = Plan_CategoriaInstalaciones.objects.filter(plan=instalacion.plan)
            cantidad_instalaciones_sin_evaluar = listado_instalaciones.count() - listado_instalaciones.exclude(estado__id=1).count()
            messages.success(request, "Instalación actualizada correctamente.")
            contexto = {       
                'instalacion':instalacion,
                'cantidad_instalaciones_sin_evaluar':cantidad_instalaciones_sin_evaluar
            }
            return render(request, 'plan_infra/actualizaInstalacionPlanHtmxPOST.html', contexto)
    contexto = {       
        'instalacion':instalacion,       
        'form': form,
    }
    return render(request, 'plan_infra/actualizaInstalacionPlanHtmxGET.html', contexto)                

def actualizaInstalacionPlanHtmxCancel(request, id_instalacion):
    instalacion = Plan_CategoriaInstalaciones.objects.get(id = id_instalacion)
    listado_instalaciones = Plan_CategoriaInstalaciones.objects.filter(plan=instalacion.plan)
    cantidad_instalaciones_sin_evaluar = listado_instalaciones.count() - listado_instalaciones.exclude(estado__id=1).count()
    contexto = {       
        'instalacion':instalacion,
        'cantidad_instalaciones_sin_evaluar':cantidad_instalaciones_sin_evaluar
    }    
    return render(request, 'plan_infra/actualizaInstalacionPlanHtmxPOST.html', contexto)

# *************** CRUD Estado Recinto HTMX ****************************
@csrf_exempt 
def actualizaEstadoRecintoHtmx(request, id_recinto):
    recinto = Recinto.objects.get(id = id_recinto)    
    form = RecintoEstadoForm(instance=recinto)
    if request.method == 'POST':        
        form = RecintoEstadoForm(request.POST, instance=recinto)
        if form.is_valid():
            recinto = form.save()
            if recinto.estado.id != 1:
                boolean_estado = True
            else:
                boolean_estado = False
            messages.success(request, "Instalación actualizada correctamente.")
            contexto = {       
                'recinto':recinto,
                'boolean_estado':boolean_estado
            }
            return render(request, 'plan_infra/actualizaEstadoRecintoHtmxPOST.html', contexto)
    contexto = {       
        'recinto':recinto,       
        'form': form,
    }
    return render(request, 'plan_infra/actualizaEstadoRecintoHtmxGET.html', contexto)    
    
def actualizaEstadoRecintoHtmxCancel(request, id_recinto):
    recinto = Recinto.objects.get(id = id_recinto)
    if recinto.estado.id != 1:
        boolean_estado = True
    else:
        boolean_estado = False
    contexto = {       
        'recinto':recinto,
        'boolean_estado':boolean_estado
    }    
    return render(request, 'plan_infra/actualizaEstadoRecintoHtmxPOST.html', contexto) 

def resumenPlanInfraestructura(request, year):    
    establecimientos = Establecimiento.objects.all()
    listado_monto_mantenimiento = MontoMantenimiento.objects.filter(year=2024)
    plan_ingraestructura = PlanInfraestructura.objects.filter(year=year)
    total_mantenimiento = 0
    total_plan_infraestructura = 0
       
    for i in listado_monto_mantenimiento:
        if i.monto:
            total_mantenimiento += i.monto        
    for i in plan_ingraestructura:
        if i.total:
            total_plan_infraestructura += i.total
        
    listado = []
    for e in establecimientos:
        barra = random.randint(0, 110)         
        presupuesto = 0        
        total_plan = None
        estado_plan = None
        fecha_creacion = None        
        fecha_envio = None
        for monto in listado_monto_mantenimiento:            
            if monto.establecimiento.id == e.id:                
                presupuesto = monto.monto
        for plan in plan_ingraestructura:            
            if plan.establecimiento.id == e.id:
                total_plan = plan.total
                estado_plan = plan.estado
                fecha_creacion = plan.created
                fecha_envio = plan.fecha_envio
                
        listado.append(
            {
                'codigo': e.codigo,
                'nombre': e.nombre,
                'categoria': e.categoria.nombre ,
                'comuna': e.comuna,
                'presupuesto': presupuesto,
                'total_plan': total_plan,
                'estado_plan':estado_plan,
                'fecha_creacion':fecha_creacion,
                'fecha_envio':fecha_envio,
                'barra':barra,                       
            }
        )
    contexto = {
        'title_nav': 'Plan Infraestructura y Mantenimiento ' + str(plan.year),
        'listado':listado,
        'year':year,
        'total_mantenimiento':total_mantenimiento,
        'total_plan_infraestructura':total_plan_infraestructura
    }    
    return render(request, 'plan_infra/resumen_plan_infraestructura.html', contexto)  
        
def modalConfirmarEnvioPlan(request, id_plan, id_establecimiento):
    plan = PlanInfraestructura.objects.get(id=id_plan)
    establecimiento = Establecimiento.objects.get(id=id_establecimiento)
    contexto = {
        'plan': plan,
        'establecimiento':establecimiento        
    }
    return render(request, 'plan_infra/modal_confirmar_envio_plan.html', contexto)

def cerrarPlan(request, id_plan, id_establecimiento):
    plan = PlanInfraestructura.objects.get(id=id_plan)
    plan.estado = 2
    plan.fecha_envio = datetime.datetime.now()
    plan.save()
    messages.success(request, "Plan enviado correctamente.") 
    return redirect('detalle_plan_infra', id_plan, id_establecimiento)
