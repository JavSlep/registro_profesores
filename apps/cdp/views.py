from django.shortcuts import render, redirect
from .forms import CDPForm
import datetime
from ..establecimiento.models import Establecimiento
from ..cdp.models import *
from django.views.generic import ListView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from uuid import UUID
from django.http import Http404



# Create your views here.
class Ejemplo(ListView):
    model = Cdp
    template_name = 'ejemplo.html'

    #Modificar metodo post
    def post(self, request, *args, **kwargs):
        form = CDPForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ejemplo')
        else:
            return render(request, 'ejemplo.html', {'form': form})
class crearCdp(CreateView):
    model = Cdp
    template_name = 'crear_cdp.html'
    form_class = CDPForm

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

@csrf_exempt
def ingresar_cdp(request,year,programa):
    if programa =='none':
        programa = None
    form = CDPForm(programa=programa)
    # Si el formulario se envía por POST
    if request.method == 'POST':
        form = CDPForm(request.POST,programa=programa)
        if form.is_valid():
            
            cdp = form.save(commit=False)
            
            cdp.save()
            #La alerta me salta despues de cambiar de pagina
            messages.success(request, "CDP guardado exitosamente")
            cdps = Cdp.objects.filter(item_presupuestario__subtitulo_presupuestario__year__year=year, item_presupuestario__subtitulo_presupuestario__programa_presupuestario=programa)
            context = {
                'cdps': cdps
            }
            
            return render(request, 'listado.html', context)
    
    context = {
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
    cdp = Cdp.objects.all()
    context = {
        'cdps': cdp
    }
    return render(request, 'historial_cdp.html',context)

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
    print(f"{programa} {year}")
    # Lógica para obtener el listado de CDPs
    cdps = Cdp.objects.filter(item_presupuestario__subtitulo_presupuestario__year__year=year, item_presupuestario__subtitulo_presupuestario__programa_presupuestario=programa)
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
    
def modal_prueba(request):
    form = CDPForm()
    context= {
        'form':form,
        'cdps': Cdp.objects.all(),
        
    }
    return render(request, 'modal_prueba.html', context)

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