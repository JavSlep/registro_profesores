from django.shortcuts import render, redirect
from .forms import CDPForm
import datetime
from ..establecimiento.models import Establecimiento
from ..cdp.models import *
from django.views.generic import ListView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages



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
def cdp(request):
    # Por ejemplo, cargar los datos asociados a esa área o unidad
    year = datetime.datetime.now().year
    return render(request, 'home_funcionarios.html',{'current_year':year})

@csrf_exempt
def ingresar_cdp(request):
    form = CDPForm()
    # Si el formulario se envía por POST
    if request.method == 'POST':
        form = CDPForm(request.POST)

        if form.is_valid():
            cdp = form.save(commit=False)
            # Lógica para guardar el CDP en la base de datos
            cdp.save()
                       
            cdps = Cdp.objects.all()
            context = {
                'cdps': cdps
            }
            messages.success(request, "CDP guardado exitosamente")
            return render(request, 'historial_cdp.html', context)
        else:
            print("Error en el formulario", form.errors)

    context = {
        'form': form,
        'title_nav': 'Ingresar CDP',
    }
    # Renderizamos la página con el formulario
    return render(request, 'ingresar_cdp.html', context)

def historial_cdp(request):
    # Lógica para obtener el listado de CDPs
    if request.method == 'POST':
        ingresar_cdp(request)
    cdp = Cdp.objects.all()
    context = {
        'cdps': cdp
    }
    return render(request, 'historial_cdp.html',context)

def ley_presupuestaria(request,year):
    subtitulos_presupuestarios = SubtituloPresupuestario.objects.filter(year__year=year).order_by('subtitulo__n_subtitulo')
    print(subtitulos_presupuestarios)
    # Agrupar los subtítulos por programa_presupuestario
    subtitulos_p01 = subtitulos_presupuestarios.filter(programa_presupuestario="P01 GASTOS ADMINISTRATIVOS")
    subtitulos_p02 = subtitulos_presupuestarios.filter(programa_presupuestario="P02 SERVICIOS EDUCATIVOS")

    context = {
        'subtitulos_p01': subtitulos_p01,
        'subtitulos_p02': subtitulos_p02,
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
    current_year_value = 2026
    context={
            'current_year':current_year_value
        }
    if request.method == 'POST':
        
        # Buscar el año actual en el modelo Year
        try:
            current_year = Year.objects.get(year=current_year_value)
            for subt in Subtitulo.objects.all():
                for prog in PROGRAMAS_PRESUPUESTARIOS:
                    subtitulo = SubtituloPresupuestario.objects.create(
                        year=current_year,
                        subtitulo=subt,
                        programa_presupuestario=prog[0],
                        ley_presupuestaria_subtitulo=0,
                        )
            messages.info(request, "El año ya se ha creado anteriormente")
            return render(request,'generar_ley_presupuestaria.html',context)
        except Year.DoesNotExist:
            current_year = Year.objects.create(year=current_year_value)
            
            
            messages.success(request, f"El año presupuestario {current_year_value} se ha creado correctamente")
            return render(request,'generar_ley_presupuestaria.html',context)
    # Asegúrate de devolver un HttpResponse en caso de GET o si no se cumple ninguna condición
    return render(request, 'generar_ley_presupuestaria.html', context)
    


def listado(request):
    # Lógica para obtener el listado de CDPs
    cdps = Cdp.objects.all()
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