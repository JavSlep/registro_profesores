from django.shortcuts import render, redirect, get_object_or_404
from ..mantenimiento.models import MontoMantenimiento
from .models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.contrib import messages
from .form import Diagnostico_PartidaDiagnosticoForm, Diagnostico_CategoriaInstalacionesForm, ObservacionDiagnosticoForm
from PIL import Image, ImageDraw, ImageFont, ImageOps
from django.http import HttpResponse, JsonResponse
import uuid
from io import BytesIO
from django.http import Http404

def instruccionesDiagnostico(request, id_establecimiento):
    establecimiento = Establecimiento.objects.get(id=id_establecimiento)
    diagnostico = Diagnostico.objects.filter(establecimiento=id_establecimiento, year=2025).first()
    contexto = {
        'title_nav': 'Plan Infraestructura y Mantenimiento ' + str(2025),       
        'establecimiento':establecimiento,
        'diagnostico':diagnostico
    }
    return render(request, 'diagnostico/instrucciones_diagnostico.html', contexto)

def creacionInstalacionesDiagnostico(id_diagnostico):           
    diagnostico = Diagnostico.objects.get(id=id_diagnostico)
    listado_instalaciones = CategoriaInstalaciones.objects.all()    
    if listado_instalaciones:
        for i in listado_instalaciones:
            estado = EstadoInstalaciones.objects.filter(nombre="Sin Evaluar").first()        
            Diagnostico_CategoriaInstalaciones.objects.create (
                estado = estado,
                diagnostico = diagnostico,
                categoria_instalaciones = i,                     
            )
            
def creacionPartidaDiagnostico(id_diagnostico):           
    diagnostico = Diagnostico.objects.get(id=id_diagnostico)
    listado_partidas = PartidaDiagnostico.objects.all()    
    if listado_partidas:
        for i in listado_partidas:
            Diagnostico_PartidaDiagnostico.objects.create (
                evaluacion = 1,
                diagnostico = diagnostico,
                partida_diagnostico = i,                     
            )

def nuevoDiagnostico(request, id_establecimiento):
    establecimiento = get_object_or_404(Establecimiento, id=id_establecimiento)    
    
    diagnostico = Diagnostico.objects.create (        
        establecimiento = establecimiento,   
        nombre= "Plan de Ingraestructura y Mantenimiento 2025",
        estado = 1,
        year = 2025,
        descripcion = 'Plan 2025'
    )
    creacionInstalacionesDiagnostico(diagnostico.id)
    creacionPartidaDiagnostico(diagnostico.id)
    messages.success(request, "Plan creado correctamente.")    
    return redirect('editar_diagnostico', diagnostico.id, establecimiento.id)

def detalleDiagnostico(request, id_diagnostico, id_establecimiento):
    diagnostico = Diagnostico.objects.get(id=id_diagnostico)
    establecimiento = Establecimiento.objects.get(id=id_establecimiento)
    listado_instalaciones = Diagnostico_CategoriaInstalaciones.objects.filter(diagnostico=diagnostico)
    listado_partidas = Diagnostico_PartidaDiagnostico.objects.filter(diagnostico=diagnostico)
    contexto = {
        'title_nav': 'Plan Infraestructura y Mantenimiento ' + str(diagnostico.year),        
        'establecimiento':establecimiento,
        'diagnostico':diagnostico,
        'listado_instalaciones':listado_instalaciones,
        'listado_partidas':listado_partidas
    }
    return render(request, 'diagnostico/detalle_diagnostico.html', contexto)

def editarDiagnostico(request, id_diagnostico, id_establecimiento):
    current_date = date.today()  
    year =  current_date.year
    diagnostico = Diagnostico.objects.get(id=id_diagnostico)        
    establecimiento =  Establecimiento.objects.get(id=id_establecimiento)    
    monto_mantenimiento_asignado =  MontoMantenimiento.objects.filter(establecimiento=id_establecimiento, year=2024).first() 
    if monto_mantenimiento_asignado:
        monto_mantenimiento_asignado = monto_mantenimiento_asignado.monto
    else:
        monto_mantenimiento_asignado = 0
    listado_instalaciones = Diagnostico_CategoriaInstalaciones.objects.filter(diagnostico=diagnostico)    
    cantidad_instalaciones_sin_evaluar = listado_instalaciones.count() - listado_instalaciones.exclude(estado__id=1).count()
    listado_partidas = Diagnostico_PartidaDiagnostico.objects.filter(diagnostico=diagnostico)
    cantidad_partidas = listado_partidas.count()
    cantidad_partidas_evaluadas = listado_partidas.exclude(evaluacion=1).count()    
    cantidad_partidas_sin_evaluar = cantidad_partidas - cantidad_partidas_evaluadas
    listado_titulos_item = TituloItemDiagnostico.objects.all()    
    listado_item = ItemDiagnostico.objects.all().order_by('orden')
    contexto = {
        'title_nav': 'Plan Infraestructura y Mantenimiento ' + str(diagnostico.year),
        'diagnostico':diagnostico,
        'monto_mantenimiento_asignado':monto_mantenimiento_asignado,       
        'establecimiento':establecimiento,     
        'listado_instalaciones':listado_instalaciones,
        'cantidad_instalaciones_sin_evaluar':cantidad_instalaciones_sin_evaluar,
        'listado_partidas':listado_partidas,
        'cantidad_partidas_sin_evaluar':cantidad_partidas_sin_evaluar,
        'listado_titulos_item':listado_titulos_item,
        'listado_item':listado_item,       
       
    }
    return render(request, 'diagnostico/editar_diagnostico.html', contexto)

@csrf_exempt 
def actualizaPartidaDiagnosticoHtmx(request, id_partida):    
    partida = Diagnostico_PartidaDiagnostico.objects.get(id = id_partida) 
    form = Diagnostico_PartidaDiagnosticoForm(instance=partida)    
    if request.method == 'POST':        
        form = Diagnostico_PartidaDiagnosticoForm(request.POST, instance=partida)        
        if form.is_valid():
            partida = form.save()
            messages.success(request, "Partida actualizada correctamente.")            
            listado_partidas = Diagnostico_PartidaDiagnostico.objects.filter(diagnostico=partida.diagnostico)
            cantidad_partidas = listado_partidas.count()
            cantidad_partidas_evaluadas = listado_partidas.exclude(evaluacion=1).count()    
            cantidad_partidas_sin_evaluar = cantidad_partidas - cantidad_partidas_evaluadas            
            contexto = {       
                'partida':partida,
                'cantidad_partidas_sin_evaluar':cantidad_partidas_sin_evaluar               
            }           
            return render(request, 'diagnostico/actualiza_partida_diagnostico_htmx_post.html', contexto)
    contexto = {       
        'partida':partida,       
        'form': form,
    }
    return render(request, 'diagnostico/actualiza_partida_diagnostico_htmx_get.html', contexto)

def actualizaPartidaDiagnosticoHtmxCancel(request, id_partida):
    partida = Diagnostico_PartidaDiagnostico.objects.get(id = id_partida)
    listado_partidas = Diagnostico_PartidaDiagnostico.objects.filter(diagnostico=partida.diagnostico)
    cantidad_partidas = listado_partidas.count()
    cantidad_partidas_evaluadas = listado_partidas.exclude(evaluacion=1).count()    
    cantidad_partidas_sin_evaluar = cantidad_partidas - cantidad_partidas_evaluadas    
    contexto = {       
        'partida':partida,
        'cantidad_partidas_sin_evaluar':cantidad_partidas_sin_evaluar        
    }    
    return render(request, 'diagnostico/actualiza_partida_diagnostico_htmx_post.html', contexto)

def modalConfirmarEnvioDiagnostico(request, id_diagnostico, id_establecimiento):
    diagnostico = Diagnostico.objects.get(id=id_diagnostico)
    establecimiento = Establecimiento.objects.get(id=id_establecimiento)    
    listado_partidas = Diagnostico_PartidaDiagnostico.objects.filter(diagnostico=id_diagnostico)
    cantidad_partidas = listado_partidas.count()
    cantidad_partidas_evaluadas = listado_partidas.exclude(evaluacion=1).count()    
    cantidad_partidas_sin_evaluar = cantidad_partidas - cantidad_partidas_evaluadas    
    cantidad_fotos_subidas = ImagenDiagnostico.objects.filter(diagnostico=id_diagnostico).count()
    cantidad_fotos_faltantes = 12 - cantidad_fotos_subidas    
    listado_instalaciones = Diagnostico_CategoriaInstalaciones.objects.filter(diagnostico=id_diagnostico)            
    cantidad_instalaciones_sin_evaluar = listado_instalaciones.count() - listado_instalaciones.exclude(estado__id=1).count()    
    contexto = {
        'diagnostico': diagnostico,
        'establecimiento':establecimiento,
        'cantidad_partidas_sin_evaluar':cantidad_partidas_sin_evaluar,
        'cantidad_instalaciones_sin_evaluar':cantidad_instalaciones_sin_evaluar,
        'cantidad_fotos_faltantes':cantidad_fotos_faltantes     
    }
    return render(request, 'diagnostico/modal_confirmar_envio_diagnostico.html', contexto)

def cerrarDiagnostico(request, id_diagnostico, id_establecimiento):
    diagnostico = Diagnostico.objects.get(id=id_diagnostico)
    diagnostico.estado = 2
    diagnostico.fecha_envio = datetime.datetime.now()
    diagnostico.save()
    messages.success(request, "Plan enviado correctamente.") 
    return redirect('editar_diagnostico', id_diagnostico, id_establecimiento)

def subirImagenDiagnostico(request):
    if request.method == 'POST':
        try:                    
            file = request.FILES.get('imagen')           
            id_diagnistico = request.POST['id_diagnostico']            
            diagnostico = get_object_or_404(Diagnostico, id=id_diagnistico) 
            img = Image.open(file)            
            ancho, alto = img.size
            if ancho > alto:                           
                nuevo_alto = 500
                nuevo_ancho = int((ancho/alto) * nuevo_alto)
                img = img.resize((nuevo_ancho, nuevo_alto))                                   
            elif alto > ancho:                       
                nuevo_ancho = 500
                nuevo_alto = int((alto/ancho) * nuevo_ancho )
                img = img.resize((nuevo_ancho, nuevo_alto))                                  
            else:               
                img.thumbnail((500, 500))                           
            buffer = BytesIO() 
            img.save(buffer, format='JPEG', optimize=True, quality=60)
            buffer.seek(0)            
            name = str(uuid.uuid4()) + '.jpg'        
            imagen = ImagenDiagnostico.objects.create(            
                diagnostico = diagnostico,
            )
            imagen.imagen.save(name, buffer)
            return HttpResponse('')
        except Exception as e:
            print(e)
            return JsonResponse({'post':'false'})
       
def listadoImagenesDiagnosticoHtmx(request, id_diagnostico):    
    estado_diagnostico = Diagnostico.objects.get(id=id_diagnostico).estado
    fotos = ImagenDiagnostico.objects.filter(diagnostico=id_diagnostico).order_by('-created')
    cantidad_fotos_subidas = fotos.count()    
    cantidad_fotos_faltantes = 12 - cantidad_fotos_subidas
    contexto = {
        'estado_diagnostico': estado_diagnostico,
        'fotos':fotos,
        'cantidad_fotos_faltantes':cantidad_fotos_faltantes     
    }
    return render(request, 'diagnostico/listado_imagenes_diagnostico_htmx.html', contexto)

def eliminarImagenDiagnosticoHtmx(request, id_imagen):
    try:
        foto = ImagenDiagnostico.objects.get(id=id_imagen)
    except ImagenDiagnostico.DoesNotExist:
        raise Http404("La imagen no existe.")
    id_diagnostico = foto.diagnostico.id
    foto.delete()    
    cantidad_fotos_subidas = ImagenDiagnostico.objects.filter(diagnostico=id_diagnostico).count()
    cantidad_fotos_faltantes = 12 - cantidad_fotos_subidas
    contexto = {
        'cantidad_fotos_faltantes':cantidad_fotos_faltantes,
        'id_imagen':id_imagen
    }
    return render(request, 'diagnostico/eliminar_imagen_diagnostico_htmx.html', contexto)

@csrf_exempt 
def actualizaInstalacionDiagnosticoHtmx(request, id_instalacion):    
    instalacion = Diagnostico_CategoriaInstalaciones.objects.get(id = id_instalacion)    
    form = Diagnostico_CategoriaInstalacionesForm(instance=instalacion)
    if request.method == 'POST':        
        form = Diagnostico_CategoriaInstalacionesForm(request.POST, instance=instalacion)
        if form.is_valid():
            instalacion = form.save()            
            listado_instalaciones = Diagnostico_CategoriaInstalaciones.objects.filter(diagnostico=instalacion.diagnostico)            
            cantidad_instalaciones_sin_evaluar = listado_instalaciones.count() - listado_instalaciones.exclude(estado__id=1).count()
            messages.success(request, "Instalación actualizada correctamente.")
            contexto = {       
                'instalacion':instalacion,
                'cantidad_instalaciones_sin_evaluar':cantidad_instalaciones_sin_evaluar
            }
            return render(request, 'diagnostico/actualiza_instalacion_diagnostico_htmx_post.html', contexto)
    contexto = {       
        'instalacion':instalacion,       
        'form': form,
    }
    return render(request, 'diagnostico/actualiza_instalacion_diagnostico_htmx_get.html', contexto)

def actualizaInstalacionDiagnosticoHtmxCancel(request, id_instalacion):
    instalacion = Diagnostico_CategoriaInstalaciones.objects.get(id = id_instalacion)    
    listado_instalaciones = Diagnostico_CategoriaInstalaciones.objects.filter(diagnostico=instalacion.diagnostico)     
    cantidad_instalaciones_sin_evaluar = listado_instalaciones.count() - listado_instalaciones.exclude(estado__id=1).count()    
    contexto = {       
        'instalacion':instalacion,
        'cantidad_instalaciones_sin_evaluar':cantidad_instalaciones_sin_evaluar
    }    
    return render(request, 'diagnostico/actualiza_instalacion_diagnostico_htmx_post.html', contexto)

@csrf_exempt 
def actualizaObservacionDiagnosticoHtmx(request, id_diagnostico):
    diagnostico = Diagnostico.objects.get(id = id_diagnostico)    
    form = ObservacionDiagnosticoForm(instance=diagnostico)
    if request.method == 'POST':        
        form = ObservacionDiagnosticoForm(request.POST, instance=diagnostico)
        if form.is_valid():
            diagnostico = form.save()
            messages.success(request, "Observación actualizada correctamente.")
            contexto = {       
                'diagnostico':diagnostico,
            }
            return render(request, 'diagnostico/actualiza_observacion_diagnostico_htmx_post.html', contexto)
    contexto = {       
        'diagnostico':diagnostico,       
        'form': form,
    }
    return render(request, 'diagnostico/actualiza_observacion_diagnostico_htmx_get.html', contexto)

def actualizaObservacionDiagnosticoHtmxCancel(request, id_diagnostico):
    diagnostico = Diagnostico.objects.get(id = id_diagnostico)    
    contexto = {       
        'diagnostico':diagnostico,
    }    
    return render(request, 'diagnostico/actualiza_observacion_diagnostico_htmx_post.html', contexto)
