from django.shortcuts import render, redirect
import re
from django.contrib import messages
from .forms import *
# Create your views here.

def validar_rut(rut):
    rut_limpio = rut.replace('.','').replace('-','')
    ultimo_digito = rut[-1]
    rut_limpio_sin_ultimo_digito = rut_limpio[:-1]
    rut_limpio_sin_ultimo_digito = rut_limpio_sin_ultimo_digito[::-1]
    sumador = 0
    list = [2,3,4,5,6,7]
    contador_list = 0
    for i in range(len(rut_limpio_sin_ultimo_digito)):
        number = rut_limpio_sin_ultimo_digito[i]
        valor = int(number)
        mult = valor*list[contador_list]
        contador_list += 1
        if contador_list == 6:
            contador_list = 0
        sumador += mult
    
    residuo = sumador % 11
    digito_verificador = 11 - residuo
    if digito_verificador == 11:
        digito_verificador = 0
        ultimo_digito = int(ultimo_digito)
    elif digito_verificador == 10:
        digito_verificador = 'k'
        ultimo_digito = ultimo_digito.lower()
    else:
        digito_verificador = str(digito_verificador)
    return digito_verificador == ultimo_digito
def validar_password(password,re_password):
    if not (len(password) >= 6 and len(password) <= 10):
        return False
    
    if password == re_password:
        return True

def buscar_profesor(rut):
    try:
        profesor = TeacherUser.objects.get(rut=rut)
        return profesor
    except TeacherUser.DoesNotExist:
        return None 

def registrar_profesor(request):
    if request.method == 'POST':
        form = LoginRegisterForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['rut']
            if not validar_rut(rut):
                messages.error(request, 'Ingrese un rut valido')
                return redirect('login_teacher')
            if buscar_profesor(rut):
                messages.error(request, 'El rut ingresado ya se encuentra registrado')
                return redirect('login_teacher')
            password = form.cleaned_data['password']
            confirmar_password = form.cleaned_data['confirmar_password']
            if validar_password(password,confirmar_password):
                print("Logica para crear teacher")
                profesor = TeacherUser.objects.create(rut=rut,password=password)
                messages.success(request, 'Profesor registrado con exito')
                return redirect('datos_personales', profesor.rut)
            else:
                messages.error(request, 'Error al escribir la contraseña')
                return redirect('login_teacher')
            return redirect('login_teacher')

    form = LoginRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'registrar_profesor.html', context)
def login_teacher(request):
    if request.method == 'POST':
        form_login = LoginRutForm(request.POST)
        if form_login:
            print('entro login')
            form = form_login

        if form.is_valid():
            # Accede al campo 'user' de la siguiente manera
            rut = form.cleaned_data['rut']
            
            if validar_rut(rut):
                messages.success(request, 'Rut ingresado correctamente')
                return redirect('login_teacher')
            messages.error(request, 'Rut no valido')
            return redirect('login_teacher')
    form = LoginRutForm()
    formRegister = LoginRegisterForm()

    context = {
        'form_login': form,
        'form_register': formRegister
    }
    return render(request, 'login_teacher.html', context)

def modal_password(request):
    return render(request, 'modal_password.html')


def datos_personales(request,rut):
    print(rut)
    profesor = buscar_profesor(rut)
    if profesor:
        profesor_form = ProfesorForm(initial={'rut': rut})
        direccion_form = DireccionForm()
        fecha_form = FechaForm()
    else:
        messages.error(request, "No se ha encontrado su usuario")
        return redirect('login_teacher')
    if request.method == 'POST':
        profesor_form = ProfesorForm(request.POST, request.FILES)
        profesor_form.rut = rut
        direccion_form = DireccionForm(request.POST)
        fecha_form = FechaForm(request.POST)
        if profesor_form.is_valid() and direccion_form.is_valid() and fecha_form.is_valid():
            teacher_user = buscar_profesor(rut)
            direccion = direccion_form.save()
            fecha = fecha_form.save()
            profesor = profesor_form.save(commit=False)
            profesor.direccion = direccion
            profesor.fecha_nacimiento = fecha
            profesor.teacher_user = teacher_user
            profesor.save()
            messages.success(request, 'Datos personales guardados con exito')
            return redirect('datos_curriculares')  # Redirigir a una página de éxito
    
    
    context = {
        'profesor_form': profesor_form,
        'direccion_form': direccion_form,
        'fecha_form': fecha_form,
        'profesor': profesor,
    }
    return render(request, 'datos_personales.html',context)

def datos_curriculares(request):
    return render(request, 'datos_curriculares.html')

def datos_experiencia(request):
    return render(request, 'datos_experiencia.html')

def datos_tecnicos(request):
    return render(request, 'datos_tecnicos.html')

def calendario_disponibilidad(request):
    return render(request, 'calendario_disponibilidad.html')

def ranking_evaluacion(request):
    return render(request, 'ranking_evaluacion.html')

def finalizar_form(request):
    return render(request, 'finalizar_form.html')