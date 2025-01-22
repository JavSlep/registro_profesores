from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from ..establecimiento.models import Establecimiento
from django.http import Http404
from .models import FONDOS
from .models_proyeccion import *
from .forms import MesProyectadoForm


def buscar_establecimiento(filter_establecimiento):
    try:
        establecimiento = Establecimiento.objects.get(id=filter_establecimiento)
        return establecimiento
    except Establecimiento.DoesNotExist:
        return None

def ingresar_proyeccion_inicial(request,filter_establecimiento):
    print(filter_establecimiento)
    establecimientos = Establecimiento.objects.all().order_by('nombre')


    if request.method == 'POST':

        filter_establecimiento = request.POST.get('filter_establecimiento')
        filter_subvencion = request.POST.get('filter_subvencion')

        establecimiento = buscar_establecimiento(filter_establecimiento)
        if establecimiento is None:
            messages.info(request, "Seleccione un establecimiento.")
            return redirect('ingresar_proyeccion_inicial','todos')
        else:
            #Buscamos las subvenciones asociadas a la proyeccion del establecimiento
            proyeccion = ProyeccionAnual.objects.get(establecimiento=establecimiento)
            current_subvencion = None
            subvenciones = Subvencion.objects.filter(proyeccion_anual=proyeccion)
            for subvencion in subvenciones:
                if subvencion.id == filter_subvencion:
                    current_subvencion = subvencion
                    break
            #Se comprueba si se selecciono una subvencion
            if current_subvencion is None:
                messages.info(request, "Seleccione un fondo.")

                context = {
                    'filter_establecimiento': filter_establecimiento,
                    'establecimientos': establecimientos,
                    'subvenciones': subvenciones,
                    'establecimiento': establecimiento,
                }
                return render(request,'proyeccion_anual/ingresar_proyeccion_inicial.html',context)
            else:
                meses = MesProyectado.objects.filter(subvencion=current_subvencion)
                print(type(meses[0].mes))
                context = {
                    'filter_establecimiento': filter_establecimiento,
                    'filter_subvencion': filter_subvencion,
                    'establecimientos': establecimientos,
                    'subvenciones': subvenciones,
                    'establecimiento': establecimiento,
                    'meses': meses,
                    'current_subvencion': current_subvencion,
                }

                return render(request, 'proyeccion_anual/ingresar_proyeccion_inicial.html', context)

    context = {
            'filter_establecimiento': filter_establecimiento,
            'establecimientos': establecimientos,
            }
    return render(request, 'proyeccion_anual/ingresar_proyeccion_inicial.html', context)

def buscar_mes(filter_mes):
    try:
        mes = MesProyectado.objects.get(id=filter_mes)
        return mes
    except MesProyectado.DoesNotExist:
        return None

def proyeccion_anual(subvencion,current_mes):
    meses_subvencion = MesProyectado.objects.filter(subvencion=subvencion)
    if current_mes.estado == 'Estimado':
        return
    
    promedio = 0
    for i in range(len(meses_subvencion)):
        if current_mes.mes == 'Enero' or current_mes.mes == 'Febrero':
            print("Se llego hasta aca nomas "+current_mes.mes)
            break
        elif meses_subvencion[i].mes==current_mes.mes:
            for j in range(i,len(meses_subvencion)):
                if meses_subvencion[j].mes == 'Diciembre':
                    break
                else:
                    suma_meses = meses_subvencion[j-2].monto + meses_subvencion[j-1].monto + meses_subvencion[j].monto
                    promedio = round(suma_meses / 3)
                    print("Estemos en: "+meses_subvencion[j].mes+" Promedio: "+str(promedio))
                    meses_subvencion[j+1].monto = promedio
                    meses_subvencion[j+1].estado = ESTADOS_MONTO[0][1]
                    meses_subvencion[j+1].save()
            break



def modal_modificar_proyeccion(request,mes_id):
    mes = buscar_mes(mes_id)
    form = MesProyectadoForm(instance=mes)

    if request.method == 'POST':
        form = MesProyectadoForm(request.POST, instance=mes)
        
        if form.is_valid():
            #hacer logica para proyectar los meses
            form.save()
            proyeccion_anual(mes.subvencion,mes)
            context = {
                    'filter_establecimiento': mes.subvencion.proyeccion_anual.establecimiento.id,
                    'filter_subvencion': mes.subvencion.id,
                    'establecimientos': Establecimiento.objects.all().order_by('nombre'),
                    'subvenciones': Subvencion.objects.filter(proyeccion_anual=mes.subvencion.proyeccion_anual),
                    'establecimiento': mes.subvencion.proyeccion_anual.establecimiento,
                    'meses': MesProyectado.objects.filter(subvencion=mes.subvencion),
                    'current_subvencion': mes.subvencion.fondo,
                }
            return render(request, 'proyeccion_anual/ingresar_proyeccion_inicial.html',context)

    if mes:
        context = {
            'form': form,
            'mes': mes
        }
        return render(request, 'proyeccion_anual/modal_modificar_proyeccion.html', context)
        