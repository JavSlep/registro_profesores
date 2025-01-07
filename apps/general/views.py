from django.shortcuts import render
from ..establecimiento.models import Establecimiento

def index(request):
    establecimientos = Establecimiento.objects.all()
    contexto = {
        'establecimientos':establecimientos
    }
    return render(request, 'index.html', contexto)

    
