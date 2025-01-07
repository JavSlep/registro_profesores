from django.shortcuts import render, redirect
from .models import *
from ..mantenimiento.models import PartidaNomina
import datetime
from django.contrib import messages
from .form import *
    
# *********** Items ****************

def listadoItems(request):
    listado_items = Item.objects.all()
    contexto = {
        'listado_items':listado_items,
    }
    return render(request, 'items/listado_items.html', contexto)

def detalleItem(request, id_item):
    item = Item.objects.get(id=id_item)
    listado_partidas = Partida.objects.all()
    listado_partidas_ingresadas = Item_Partida.objects.filter(item=id_item)
    if request.method == "POST":      
        id_partida = request.POST['id_partida']                    
        partida = Partida.objects.get(id=id_partida)
        Item_Partida.objects.create (
            partida = partida,
            item = item
        )       
        return redirect('detalle_item', id_item)
    contexto = {
        'item':item,
        'listado_partidas':listado_partidas,
        'listado_partidas_ingresadas':listado_partidas_ingresadas
    }
    return render(request, 'items/detalle_item.html', contexto)

def eliminarItemPartidaItem(request, id_item_partida, id_item):    
    item_partida = Item_Partida.objects.get(id=id_item_partida)
    item_partida.delete()
    return redirect ('detalle_item', id_item)
  
def nuevoItem(request):
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, "Item creado correctamente.")
            return redirect ('detalle_item', item.id)
    contexto = {
        'form':form,
    }
    return render(request, 'items/nuevo_item.html', contexto)

def editarItem(request, id_item):
    item = Item.objects.get(id=id_item)
    form = ItemForm(instance=item)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            messages.success(request, "Item editado correctamente.")
            return redirect ('detalle_item', item.id)
    contexto = {
        'item':item,
        'form':form,
    }
    return render(request, 'items/editar_item.html', contexto)

def listadoPartidasItem(request):
    filtro_categoria = CategoriaPartida.objects.all()
    listado_partidas = Partida.objects.all()
    id_categoria = ""
    filter_aplicado = False
    if request.method == "POST":        
        id_categoria = request.POST['id_categoria']      
        if id_categoria:
            listado_partidas = Partida.objects.filter(categoria_partida=id_categoria)
            filter_aplicado = True
    contexto = {
        'title_nav': 'Infraestructura',
        'listado_partidas':listado_partidas,
        'filtro_categoria':filtro_categoria,
        'id_categoria':id_categoria,
        'filter_aplicado':filter_aplicado
    }
    return render(request, 'items/listado_partidas_item.html', contexto)

def nuevaPartidaItem(request):
    listado_partidas = PartidaNomina.objects.all()
    form = PartidaForm()
    if request.method == 'POST':
        form = PartidaForm(request.POST)
        if form.is_valid():
            partida = form.save()
            messages.success(request, "Partida creada correctamente.")
            return redirect ('editar_partida_item', partida.id )
    contexto = {        
        'form':form,        
        'listado_partidas':listado_partidas,       
    }
    return render(request, 'items/nueva_partida_item.html', contexto)

def editarPartidaItem(request, id_partida):    
    partida = Partida.objects.get(id=id_partida)
    
    listado_item = Item.objects.all()
    listado_item_partida_ingresados = Item_Partida.objects.filter(partida=id_partida)
    listado_partidas_mantencion = PartidaNomina.objects.all()
    listado_partidas_mantencion_ingresadas = Partida_PartidaMantencion.objects.filter(partida=id_partida)
    
    
    
    
    form = EditPartidaForm(instance=partida)
    if request.method == 'POST':
        form = EditPartidaForm(request.POST, instance=partida)
        if form.is_valid():
            partida = form.save()
            messages.success(request, "Partida editada correctamente.")
            return redirect ('listado_partidas_item')
    contexto = {        
        'form':form,
        'partida':partida,
        'listado_item':listado_item,
        'listado_item_partida_ingresados':listado_item_partida_ingresados,
        'listado_partidas_mantencion':listado_partidas_mantencion,
        'listado_partidas_mantencion_ingresadas':listado_partidas_mantencion_ingresadas       
    }
    return render(request, 'items/editar_partida_item.html', contexto)

def asociarPartidaPartidaMantencion(request, id_partida):
    partida = Partida.objects.get(id=id_partida)    
    if request.method == 'POST':
        cantidad = request.POST['cantidad']
        id_partida_mantencion = request.POST['id_partida_mantencion']
        partida_mantencion = PartidaNomina.objects.get(id=id_partida_mantencion)       
        Partida_PartidaMantencion.objects.create (
            partida = partida,
            partida_mantencion = partida_mantencion,
            cantidad = cantidad                      
        )
        messages.success(request, "Partida asociada correctamente.")
        return redirect ('editar_partida_item', id_partida)
    
def eliminarPartidaPartidaMantencion(request, id_PartidaPartidaMantencion, id_partida):
    Partida_PartidaMantencion.objects.get(id=id_PartidaPartidaMantencion).delete()
    messages.success(request, "Partida elimimada correctamente.")
    return redirect ('editar_partida_item', id_partida)


def asociarItemPartida(request, id_partida):
    partida = Partida.objects.get(id=id_partida)
    if request.method == 'POST':
        id_item = request.POST['item_seleccionado']
        item = Item.objects.get(id=id_item)
        Item_Partida.objects.create (
            partida = partida,
            item = item                       
        )
        messages.success(request, "Item asociado correctamente.")
        return redirect ('editar_partida_item', id_partida)

def eliminarItemPartida(request, id_item_partida, id_partida):
    Item_Partida.objects.get(id=id_item_partida).delete()
    messages.success(request, "Item elimimado correctamente.")
    return redirect ('editar_partida_item', id_partida)
    
def eliminarPartidaItem(request, id_partida):    
    partida = Partida.objects.get(id=id_partida)
    partida.delete()
    messages.success(request, "Partida eliminada correctamente.")
    return redirect ('listado_partidas_item')

#**********************************

def listadoCategoriaRecinto(request):
    listado_categoria_recinto = CategoriaRecinto.objects.all()
    contexto = {
        'listado_categoria_recinto':listado_categoria_recinto,
    }
    return render(request, 'categoria_recinto/listado_categoria_recinto.html', contexto)

def nuevaCategoriaRecinto(request):    
    form = CategoriaRecintoForm()
    if request.method == 'POST':
        form = CategoriaRecintoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada correctamente.")
            return redirect ('listado_categoria_recinto')
    contexto = {        
        'form':form,
    }
    return render(request, 'categoria_recinto/nueva_categoria_recinto.html', contexto)

def editarCategoriaRecinto(request, id_categoria_recinto):
    categoria = CategoriaRecinto.objects.get(id=id_categoria_recinto)    
    form = CategoriaRecintoForm(instance=categoria)
    if request.method == 'POST':
        form = CategoriaRecintoForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría editada correctamente.")
            return redirect ('listado_categoria_recinto')
    contexto = {        
        'form':form,
    }
    return render(request, 'categoria_recinto/editar_categoria_recinto.html', contexto)

def eliminarCategoriaRecinto(request, id_categoria_recinto):    
    categoria = CategoriaRecinto.objects.get(id=id_categoria_recinto)
    categoria.delete()
    messages.success(request, "Categoría eliminada correctamente.")
    return redirect ('listado_categoria_recinto')

#**********************************

def listadoTipoRecinto(request):
    listado_tipo_recinto = TipoRecinto.objects.all()
    contexto = {
        'listado_tipo_recinto':listado_tipo_recinto,
    }
    return render(request, 'tipo_recinto/listado_tipo_recinto.html', contexto)

def nuevoTipoRecinto(request):
    listado_categoria = CategoriaRecinto.objects.all()    
    form = TipoRecintoForm()
    if request.method == 'POST':
        form = TipoRecintoForm(request.POST)
        if form.is_valid():
            tipo_recinto = form.save()
            messages.success(request, "Tipo de Recinto creado correctamente.")
            return redirect ('detalle_tipo_recinto', tipo_recinto.id)
    contexto = {        
        'form':form,
        'listado_categoria':listado_categoria
    }
    return render(request, 'tipo_recinto/nuevo_tipo_recinto.html', contexto)

def detalleTipoRecinto(request, id_tipo_recinto):
    tipo_recinto = TipoRecinto.objects.get(id=id_tipo_recinto)       
    listado_items = Item.objects.all()
    listado_items_ingresados = TipoRecinto_Item.objects.filter(tipo_recinto=id_tipo_recinto)    
    if request.method == "POST": 
        id_item = request.POST['id_item']                    
        item = Item.objects.get(id=id_item)
        TipoRecinto_Item.objects.create (
            tipo_recinto = tipo_recinto,
            item = item
        )
        return redirect('detalle_tipo_recinto', id_tipo_recinto)
    contexto = {
        'tipo_recinto':tipo_recinto,
        'listado_items':listado_items,
        'listado_items_ingresados':listado_items_ingresados
    }
    return render(request, 'tipo_recinto/detalle_tipo_recinto.html', contexto)

def eliminarTipoRecintoItem(request, id_tipo_recinto_item, id_tipo_recinto):
    tipo_recinto_item = TipoRecinto_Item.objects.get(id=id_tipo_recinto_item)
    tipo_recinto_item.delete()
    return redirect ('detalle_tipo_recinto', id_tipo_recinto)

def editarTipoRecinto(request, id_tipo_recinto):
    tipo_recinto = TipoRecinto.objects.get(id=id_tipo_recinto)
    form = TipoRecintoForm(instance=tipo_recinto)
    if request.method == 'POST':
        form = TipoRecintoForm(request.POST, instance=tipo_recinto)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de Recinto editado correctamente.")
            return redirect ('listado_tipo_recinto')
    contexto = {        
        'form':form,
        'tipo_recinto':tipo_recinto
    }
    return render(request, 'tipo_recinto/editar_tipo_recinto.html', contexto)

def eliminarTipoRecinto(request, id_tipo_recinto):    
    tipo_recinto = TipoRecinto.objects.get(id=id_tipo_recinto)
    tipo_recinto.delete()
    messages.success(request, "Tipo de Recinto eliminado correctamente.")
    return redirect ('listado_tipo_recinto')

