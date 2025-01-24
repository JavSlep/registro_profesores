import datetime
from django.shortcuts import render, redirect
from django.contrib import messages

def creacion_usuarios(request):
    context = {
        'title_nav': 'Creación de usuarios',
    }
    return render(request, 'creacion_privilegios/creacion_usuarios.html', context)