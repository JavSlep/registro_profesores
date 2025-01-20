from django.shortcuts import render, redirect
from .forms import *
import datetime
from ..establecimiento.models import Establecimiento
from ..cdp.models import *
from django.views.generic import ListView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from uuid import UUID
from django.http import Http404



# Create your views here.

# Vista 'cdp'
def cdp(request,programa):
    # Por ejemplo, cargar los datos asociados a esa área o unidad
    year = datetime.datetime.now().year
    
    programas_presupuestarios = [('none', '---')] + list(PROGRAMAS_PRESUPUESTARIOS)

    try:
        year_in_db = Year.objects.get(year=year)
    except Year.DoesNotExist:
        # Si no hay year en la base de datos
        messages.error(request, f"Debes generar el inicio del año {year} en el sistema (Boton rojo)")
        context ={
        'current_year':year,
        'current_program':programa,
        'programs': programas_presupuestarios,
        'state': True
        }
        return render(request, 'home_funcionarios.html',context)
 
    context ={
        'current_year':year,
        'current_program':programa,
        'programs': programas_presupuestarios,
    }
    return render(request, 'home_funcionarios.html',context)

def ver_cdp(request,year):
    cdps = Cdp.objects.all().order_by('cdp')

    filter_year = year
    filter_program = 'todos'
    filter_establecimiento = 'todos'
    filter_unidad = 'todos'

    if request.method == 'POST':
        cdps = Cdp.objects.all().order_by('cdp')
        year = request.POST.get('filter_year')
        program = request.POST.get('filter_program')
        establecimiento = request.POST.get('filter_establecimiento')
        unidad = request.POST.get('filter_unidad')
        if year != '0':
            cdps = cdps.filter(item_presupuestario__subtitulo_presupuestario__year__year=year)
            filter_year = year

        if program != 'todos':
            cdps = cdps.filter(item_presupuestario__subtitulo_presupuestario__programa_presupuestario=program)
            filter_program = program

        if establecimiento != 'todos':
            cdps = cdps.filter(establecimiento=establecimiento)
            filter_establecimiento = establecimiento

        if unidad != 'todos':
            cdps = cdps.filter(unidad=unidad)
            filter_unidad = unidad
        context = {
            'filter_year': filter_year,
            'filter_program': filter_program,
            'filter_establecimiento': filter_establecimiento,
            'filter_unidad': filter_unidad,
            'programs': PROGRAMAS_PRESUPUESTARIOS,
            'unidades': Unidad.objects.all().order_by('nombre'),
            'establecimientos': Establecimiento.objects.all().order_by('nombre'),
            'years': Year.objects.all().order_by('year'),
            'cdps': cdps
        }
        return render(request, 'ver_cdps.html', context)
        
    cdps = cdps.filter(year_presupuestario=filter_year)

    context = {
        'filter_year': str(year),
        'filter_program': filter_program,
        'filter_establecimiento': filter_establecimiento,
        'filter_unidad': filter_unidad,
        'unidades': Unidad.objects.all().order_by('nombre'),
        'programs': PROGRAMAS_PRESUPUESTARIOS,
        'establecimientos': Establecimiento.objects.all().order_by('nombre'),
        'years': Year.objects.all().order_by('year'),
        'cdps': cdps
    }
    return render(request, 'ver_cdps.html', context)

@csrf_exempt
def ingresar_cdp(request,year,programa):
    titulo =""
    if programa == 'P01 GASTOS ADMINISTRATIVOS':
        titulo = 'Ingresar CDP Unidad'
        form = CDPFormUnidad()
        form.fields['estado'].initial = 'ingresado'
        form.fields['estado'].choices = [item for item in form.fields['estado'].choices if item[0] == 'ingresado']
    elif programa =='P02 SERVICIOS EDUCATIVOS':
        titulo = 'Ingresar CDP Establecimiento'
        form = CDPFormEstablecimiento()
        form.fields['estado'].initial = 'ingresado'
        form.fields['estado'].choices = [item for item in form.fields['estado'].choices if item[0] == 'ingresado']
    else:
        titulo = 'Seleccione un programa'
        form = None
    
    # Si el formulario se envía por POST
    if request.method == 'POST':
        if programa == 'P01 GASTOS ADMINISTRATIVOS':
            form = CDPFormUnidad(request.POST)
        elif programa =='P02 SERVICIOS EDUCATIVOS':
            form = CDPFormEstablecimiento(request.POST)
        else:
            programa=None
        
        form.fields['estado'].initial = 'ingresado'
        if form.is_valid():
            cdp = form.save(commit=False)
            cdp.save()
            #La alerta me salta despues de cambiar de pagina
            messages.success(request, "CDP guardado exitosamente")
            cdps = Cdp.objects.filter(year_presupuestario=year, item_presupuestario__subtitulo_presupuestario__programa_presupuestario=programa).order_by('cdp')
            context = {
                'cdps': cdps,
            }
            
            return render(request, 'listado.html', context)
    context = {
        'titulo_cdp': titulo,
        'form': form,
        'current_program': programa,
        'current_year': year,
        'title_nav': 'Ingresar CDP',
    }
    # Renderizamos la página con el formulario
    return render(request, 'ingresar_cdp.html', context)

def historial_cdp(request):
    if request.method == 'POST':
        ingresar_cdp(request)
    cdp = Cdp.objects.all().order_by('cdp')
    context = {
        'cdps': cdp
    }
    return render(request, 'historial_cdp.html',context)

def historial_cdp_general(request,year):
    cdps = Cdp.objects.all()
    subtitulo ="Filtros aplicados"

    filter_year = year
    filter_program = 'todos'
    filter_estado = 'todos'
    filter_establecimiento = 'todos'
    filter_unidad = 'todos'
    filtros = []

    if request.method == 'POST':
        cdps = Cdp.objects.all()
        year = request.POST.get('filter_year')
        program = request.POST.get('filter_program')
        estados = request.POST.getlist('filter_estado')
        print(estados)
        establecimiento = request.POST.get('filter_establecimiento')
        unidad = request.POST.get('filter_unidad')
        if year != '0':
            cdps = cdps.filter(item_presupuestario__subtitulo_presupuestario__year__year=year)
            filter_year = year
            filtros.append(f"Año: {year}")

        if program != 'todos':
            cdps = cdps.filter(item_presupuestario__subtitulo_presupuestario__programa_presupuestario=program)
            filter_program = program
            filtros.append(f"Programa: {program}")

        filtro_estados = "Estado/s:"
        for estado in estados:
            if estado == 'todos':
                break
            else:
                cdps = cdps.filter(estado__in=estados)
                filter_estado = estados
                filtro_estados +=(f" {estado.upper()}")
        if filtro_estados != "Estado/s:":
            filtros.append(filtro_estados)
        
            

        if establecimiento != 'todos':
            cdps = cdps.filter(establecimiento=establecimiento)
            filter_establecimiento = establecimiento
            establecimiento_nombre = Establecimiento.objects.get(id=establecimiento).nombre
            if establecimiento_nombre.__len__() > 30:
                filtros.append(f"Establecimiento: {establecimiento_nombre[:30]}...")
            else:
                filtros.append(f"Establecimiento: {establecimiento_nombre}")
            

        if unidad != 'todos':
            cdps = cdps.filter(unidad=unidad)
            filter_unidad = unidad
            unidad = Unidad.objects.get(id=unidad)
            filtros.append(f"Unidad: {unidad}")

        context = {
            'subtitulo': subtitulo,
            'filter_year': filter_year,
            'filter_program': filter_program,
            'filter_estado': filter_estado,
            'filter_establecimiento': filter_establecimiento,
            'filter_unidad': filter_unidad,
            'filtros': filtros,
            'estados': ESTADOS,
            'programs': PROGRAMAS_PRESUPUESTARIOS,
            'unidades': Unidad.objects.all().order_by('nombre'),
            'establecimientos': Establecimiento.objects.all().order_by('nombre'),
            'years': Year.objects.all().order_by('year'),
            'cdps': cdps.order_by('-cdp')
        }
        return render(request, 'historial_cdp_general.html', context)
        
    cdps = cdps.filter(year_presupuestario=filter_year)
    filtros.append(filter_year)
    context = {
        'subtitulo': subtitulo,
        'filter_year': str(year),
        'filter_program': filter_program,
        'filter_establecimiento': filter_establecimiento,
        'filter_unidad': filter_unidad,
        'filtros': filtros,
        'estados': ESTADOS,
        'programs': PROGRAMAS_PRESUPUESTARIOS,
        'establecimientos': Establecimiento.objects.all().order_by('nombre'),
        'unidades': Unidad.objects.all().order_by('nombre'),
        'years': Year.objects.all().order_by('year'),
        'cdps': cdps.order_by('-cdp')
    }
    return render(request, 'historial_cdp_general.html', context)

def historial_items(request, id):
    
    try:
        item = ItemPresupuestario.objects.get(id=id)
    except ValueError:
        raise ValueError("El ID proporcionado no es un UUID válido")
    except Item.DoesNotExist:
        raise ValueError("El ítem con el ID proporcionado no existe")

    cdps_items = Cdp.objects.filter(item_presupuestario=item)
    context = {
        'item': item,
        'cdps_items': cdps_items
    }
    return render(request, 'modal_prueba.html', context)

def ley_presupuestaria(request,year):
    subtitulos_presupuestarios = SubtituloPresupuestario.objects.filter(year__year=year).order_by('subtitulo__n_subtitulo')
    items = ItemPresupuestario.objects.filter(subtitulo_presupuestario__year__year=year).order_by('item__n_item')
    cdps = Cdp.objects.filter(item_presupuestario__subtitulo_presupuestario__year__year=year).order_by('item_presupuestario__subtitulo_presupuestario__subtitulo__n_subtitulo')
    
    context = {
        'cdps': cdps,
        'programas': PROGRAMAS_PRESUPUESTARIOS,
        'subtitulos': subtitulos_presupuestarios,
        'items_presupuestarios': items,
        'years': Year.objects.all(),
        'current_year': year,
    }

    return render(request, 'ley_presupuestaria.html', context)

def actualizar_ley_presupuestaria(request, year):
    if request.method == 'POST':
        # Obtener los subtítulos presupuestarios para el año especificado
        subtitulos_presupuestarios = SubtituloPresupuestario.objects.filter(year__year=year)

        # Recorrer los subtítulos y actualizar los valores
        for subtitulo in subtitulos_presupuestarios:
            field_name = f'ley_presupuestaria_{subtitulo.id}'
            if field_name in request.POST:
                nuevo_valor = request.POST[field_name]
                # Eliminar los puntos y convertir a número
                nuevo_valor = nuevo_valor.replace('.', '')
                try:
                    nuevo_valor = int(nuevo_valor)  # O usa float(nuevo_valor) si es un número decimal
                except ValueError:
                    messages.error(request, f"Valor inválido para {field_name}: {nuevo_valor}")
                    return redirect('ley_presupuestaria', year)
                subtitulo.ley_presupuestaria_subtitulo = nuevo_valor
                subtitulo.save()
        messages.success(request, "Ley presupuestaria actualizada exitosamente")
        return redirect( 'ley_presupuestaria',year)

    subtitulos_presupuestarios = SubtituloPresupuestario.objects.filter(year__year=year).order_by('subtitulo__n_subtitulo')
    
    # Agrupar los subtítulos por programa_presupuestario
    subtitulos_p01 = subtitulos_presupuestarios.filter(programa_presupuestario="P01 GASTOS ADMINISTRATIVOS")
    subtitulos_p02 = subtitulos_presupuestarios.filter(programa_presupuestario="P02 SERVICIOS EDUCATIVOS")
    
    context = {
        'subtitulos_p01': subtitulos_p01,
        'subtitulos_p02': subtitulos_p02,
        'current_year': year,
    }

    return render(request, 'actualizar_ley_presupuestaria.html', context)

def actualizar_ajuste_presupuestario(request, year):
    if request.method == 'POST':
        # Obtener los subtítulos presupuestarios para el año especificado
        items_presupuestarios = ItemPresupuestario.objects.filter(subtitulo_presupuestario__year__year=year)
        for item in items_presupuestarios: print(item.ajuste_presupuestario_item)
        # Recorrer los subtítulos y actualizar los valores
        for item in items_presupuestarios:
            field_name = f'ajuste_presupuestario_{item.id}'
            if field_name in request.POST:
                nuevo_valor = request.POST[field_name]
                # Eliminar los puntos y convertir a número
                nuevo_valor = nuevo_valor.replace('.', '')
                try:
                    nuevo_valor = int(nuevo_valor)  # O usa float(nuevo_valor) si es un número decimal
                except ValueError:
                    messages.error(request, f"Valor inválido para {field_name}: {nuevo_valor}")
                    return redirect('ley_presupuestaria', year)
                item.ajuste_presupuestario_item = nuevo_valor
                item.save()
        messages.success(request, "Ajuste presupuestario actualizado exitosamente")
        return redirect( 'ley_presupuestaria',year)

    subtitulos_presupuestarios = SubtituloPresupuestario.objects.filter(year__year=year).order_by('subtitulo__n_subtitulo')
    
    # Agrupar los subtítulos por programa_presupuestario
    subtitulos_p01 = subtitulos_presupuestarios.filter(programa_presupuestario="P01 GASTOS ADMINISTRATIVOS")
    subtitulos_p02 = subtitulos_presupuestarios.filter(programa_presupuestario="P02 SERVICIOS EDUCATIVOS")
    
    context = {
        'subtitulos_p01': subtitulos_p01,
        'subtitulos_p02': subtitulos_p02,
        'subtitulos': subtitulos_presupuestarios,
        'programas': PROGRAMAS_PRESUPUESTARIOS,
        'current_year': year,
    }

    return render(request, 'actualizar_ajuste_presupuestario.html', context)

def generar_ley_presupuestaria(request):
    current_year_value = datetime.datetime.now().year
    context={
            'current_year':current_year_value
        }
    if request.method == 'POST':
        
        # Buscar el año actual en el modelo Year
        try:
            current_year = Year.objects.get(year=current_year_value)
            messages.info(request, "El año ya se ha creado anteriormente")
            return render(request,'generar_ley_presupuestaria.html',context)
        except Year.DoesNotExist:
            current_year = Year.objects.create(year=current_year_value)
            for subt in Subtitulo.objects.all():
                for prog in PROGRAMAS_PRESUPUESTARIOS:
                    subtitulo = SubtituloPresupuestario.objects.create(
                        year=current_year,
                        subtitulo=subt,
                        programa_presupuestario=prog[0],
                        ley_presupuestaria_subtitulo=0,
                        )
            messages.success(request, f"El año presupuestario {current_year_value} se ha creado correctamente")
            return render(request,'generar_ley_presupuestaria.html',context)

    return render(request, 'generar_ley_presupuestaria.html', context)
    


def listado(request,year,programa):
    # Lógica para obtener el listado de CDPs
    if programa != 'none':
        print("Es distinto de none")
        cdps = Cdp.objects.filter(year_presupuestario=year, item_presupuestario__subtitulo_presupuestario__programa_presupuestario=programa).order_by('cdp')
    else:
        cdps = Cdp.objects.filter(year_presupuestario=year).order_by('cdp')
        
    context = {
        'cdps': cdps
    }
    return render(request, 'listado.html', context)


def subir_archivo(request):
    if request.method == 'POST':
        
        file = request.FILES['file']
        if file:
            nombre = file._name
            id_relacion = request.POST.get('id_relacion')

            Files.objects.create(
                nombre=nombre,
                file=file,
                id_relacion=id_relacion
            )
            return redirect('home_funcionarios',id_relacion)

def cambiar_year(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        
        return redirect( 'ley_presupuestaria',year)

def cambiar_programa(request):
    if request.method == 'POST':
        programa = request.POST.get('programa')
        
        return redirect( 'home_funcionarios',programa)
    

def modal_cdps_item_ley_presupuestaria(request,item_presupuestario_id):
    
    try:
        item_presupuestario = ItemPresupuestario.objects.get(id=item_presupuestario_id)
    except ItemPresupuestario.DoesNotExist:
        raise Http404("El ítem presupuestario no existe.")
    cdps = Cdp.objects.filter(item_presupuestario=item_presupuestario)
    context= {
        'cdps': cdps,
        'item_presupuestario': item_presupuestario,
        'programas': PROGRAMAS_PRESUPUESTARIOS,
    }
    return render(request, 'modal_cdps_item_ley_presupuestaria.html', context)

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404
from .forms import CDPFormUnidad, CDPFormEstablecimiento
from .models import Cdp

def modal_actualizar_cdp(request, cdp_id):
    cdp = get_object_or_404(Cdp, id=cdp_id)
    # Decidir cuál formulario usar basado en el programa presupuestario
    if cdp.unidad:
        FormClass = CDPFormUnidad
    elif cdp.establecimiento:
        FormClass = CDPFormEstablecimiento
    else:
        raise Http404("No se puede determinar el formulario adecuado para este CDP.")

    if request.method == 'POST':
        form = FormClass(request.POST, instance=cdp)
        print("Entro al post")
        if form.is_valid():
            print("El formulario es vlaidos")
            cdp = form.save()
            
            # Redirigir o devolver respuesta exitosa
            return redirect('historial_cdp_general',cdp.year_presupuestario) # Cambia a la URL deseada
    else:
        form = FormClass(instance=cdp)
    program = cdp.item_presupuestario.subtitulo_presupuestario.programa_presupuestario
    context = {
        'current_program': program,
        'form': form,
        'cdp': cdp,
    }
    return render(request, 'modal_actualizar_cdp.html', context)
