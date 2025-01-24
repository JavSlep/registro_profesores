from django.shortcuts import render, redirect
from .forms import ItemPresupuestarioForm
from django.contrib import messages
from .models import ItemPresupuestario, PROGRAMAS_PRESUPUESTARIOS, SubtituloPresupuestario
from django.shortcuts import get_object_or_404


def ingresar_item_presupuestario(request):
    form = ItemPresupuestarioForm()

    if request.method == 'POST':
        form = ItemPresupuestarioForm(request.POST)
        if form.is_valid():
            # Verificar si el item ya existe
            item_presupuestario = form.save(commit=False)
            for item in item_presupuestario.subtitulo_presupuestario.items_presupuestarios.all():
                if item.item == item_presupuestario.item:
                    messages.error(request, "El item ya existe.")
                    return redirect('ingresar_item_presupuestario')

            if not item_presupuestario.item.subtitulo.n_subtitulo == item_presupuestario.subtitulo_presupuestario.subtitulo.n_subtitulo:
                messages.error(request, f"El item {item_presupuestario.item} no pertenece al mismo subtitulo {item_presupuestario.subtitulo_presupuestario.subtitulo}.")
                return redirect('ingresar_item_presupuestario')
            item_presupuestario.save()
            messages.success(request, "Item creado correctamente.")
            return redirect('ingresar_item_presupuestario')
    context = {
        'form': form,
        'title_nav': 'Ingresar ítems',
    }
    return render(request, 'ingresar_item_presupuestario.html', context)

def modificar_items(request,year):
    subtitulos_presupuestarios = SubtituloPresupuestario.objects.filter(year__year=year).order_by('subtitulo__n_subtitulo')
    items = ItemPresupuestario.objects.filter(subtitulo_presupuestario__year__year=year).order_by('subtitulo_presupuestario__subtitulo__n_subtitulo', 'item__n_item')
    programs = PROGRAMAS_PRESUPUESTARIOS
    context = {
        'subtitulos_presupuestarios': subtitulos_presupuestarios,
        'items': items,
        'programs': programs,
        'title_nav': 'Modificar ítems',
    }
    return render(request, 'modificar_items.html', context)

def modal_modificar_item(request, item_presupuestario_id):
    item_presupuestario = get_object_or_404(ItemPresupuestario, id=item_presupuestario_id)
    form = ItemPresupuestarioForm(instance=item_presupuestario)
    

    if request.method == 'POST':
        form = ItemPresupuestarioForm(request.POST, instance=item_presupuestario)
        if form.is_valid():
            item_presupuestario = get_object_or_404(ItemPresupuestario, id=item_presupuestario_id)
            item_presupuestario_form = form.save(commit=False)

            if item_presupuestario.subtitulo_presupuestario != item_presupuestario_form.subtitulo_presupuestario:
                messages.error(request, f"El item {item_presupuestario.item} Se le ha modificado el subtitulo: {item_presupuestario.subtitulo_presupuestario.subtitulo}.")
                return redirect('modificar_items', request.session['usuario_entidad'].get('year'))
            if item_presupuestario.item != item_presupuestario_form.item:
                messages.error(request, f"El item {item_presupuestario.item} no pertenece al mismo subtitulo {item_presupuestario.subtitulo_presupuestario.subtitulo}.")
                return redirect('modificar_items', request.session['usuario_entidad'].get('year'))

            item_presupuestario_form.save()
            messages.success(request, "Item creado correctamente.")
            return redirect('modificar_items', request.session['usuario_entidad'].get('year'))
    context = {
        'form': form,
        'item_presupuestario': item_presupuestario
    }
    return render(request, 'modal_modificar_item.html', context)