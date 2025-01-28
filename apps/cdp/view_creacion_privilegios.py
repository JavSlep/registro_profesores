import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .formsUsuario import *

def creacion_usuarios(request):
    form = UserCargoForm()
    personal = UsuarioEntidad.objects.filter(area_unidad__isnull=False)
    if request.method == 'POST':
        form = UserCargoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado con exito')
            return redirect('creacion_usuarios')

    context = {
        'form': form,
        'personal': personal,
        'title_nav': 'Asignar privilegios',
    }
    return render(request, 'creacion_privilegios/creacion_usuarios.html', context)

def buscar_usuario( user_id):
    try:
        user = UsuarioEntidad.objects.get(id=user_id)
        return user
    except:
        return None
def modal_asignar_rol(request, user_id):
    print(str(user_id)+ "Estoy por el modal ")
    user = buscar_usuario(user_id)
    print(user)
    if user is None:
        return redirect('creacion_usuarios')
    
    form = UserCargoForm(instance=user)
    if request.method == 'POST':
        form = UserCargoForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rol asignado con exito')
            return redirect('creacion_usuarios')

    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'creacion_privilegios/modal_asignar_rol.html', context)