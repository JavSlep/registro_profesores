from django.urls import path, include
from .views import *
from . import view_excel
from django.contrib.auth.decorators import login_required as loguin_required



# URL Diagnostico
urlpatterns = [
    path('home/<str:programa>', loguin_required(cdp), name='home_funcionarios'),
    path('ingresar-cdp/<int:year>/<str:programa>', ingresar_cdp, name='ingresar_cdp'),
    path('listado/<int:year>/<str:programa>', listado, name='listado'),
    path('ejemplo', Ejemplo.as_view(), name='ejemplo'),
    path('historial_cdp/', historial_cdp, name='historial_cdp'),
    path('ley_presupuestaria/<int:year>',ley_presupuestaria, name='ley_presupuestaria'),
    path('actualizar_ley_presupuestaria/<int:year>',actualizar_ley_presupuestaria, name='actualizar_ley_presupuestaria'),
    path('generar_ley_presupuestaria',generar_ley_presupuestaria, name='generar_ley_presupuestaria'),
    path('cambiar_year',cambiar_year, name='cambiar_year'),
    path('cambiar_programa',cambiar_programa, name='cambiar_programa'),
]

urlpatterns += [
    path('historial_items/<uuid:id>', historial_items, name='historial_items'),
    path('modal_prueba/', modal_prueba, name='modal_prueba'),
    path('modal_cdps_item_ley_presupuestaria/<uuid:item_presupuestario_id>', modal_cdps_item_ley_presupuestaria, name='modal_cdps_item_ley_presupuestaria'),
]

# URL excel
urlpatterns += [
    path('export_subtitulos/', view_excel.export_subtitulos_to_excel, name='export_subtitulos'),
    path('subir-archivo/', subir_archivo, name='subir_archivo'),
]



