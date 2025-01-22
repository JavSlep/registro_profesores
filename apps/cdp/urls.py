from django.urls import path, include
from .views import *
from .view_excel import *
from .view_items import *
from .view_proyeccion_anual import *
from django.contrib.auth.decorators import login_required as loguin_required



# URL Diagnostico
urlpatterns = [
    path('home/<int:year>/<str:programa>', loguin_required(cdp), name='home_funcionarios'),
    path('ingresar-cdp/<int:year>/<str:programa>', ingresar_cdp, name='ingresar_cdp'),
    path('ver-cdp/<int:year>', ver_cdp, name='ver_cdp'),
    path('listado/<int:year>/<str:programa>', listado, name='listado'),
    path('historial_cdp/', historial_cdp, name='historial_cdp'),
    path('historial_cdp_general/<int:year>', historial_cdp_general, name='historial_cdp_general'),
    path('ley_presupuestaria/<int:year>',ley_presupuestaria, name='ley_presupuestaria'),
    path('actualizar_ley_presupuestaria/<int:year>',actualizar_ley_presupuestaria, name='actualizar_ley_presupuestaria'),
    path('actualizar_ajuste_presupuestario/<int:year>',actualizar_ajuste_presupuestario, name='actualizar_ajuste_presupuestario'),
    path('generar_ley_presupuestaria',generar_ley_presupuestaria, name='generar_ley_presupuestaria'),
    path('cambiar_year',cambiar_year, name='cambiar_year'),
    path('cambiar_year_actualizar_ley_presupuestaria',cambiar_year_actualizar_ley_presupuestaria, name='cambiar_year_actualizar_ley_presupuestaria'),
    path('cambiar_year_actualizar_ajuste_presupuestario',cambiar_year_actualizar_ajuste_presupuestario, name='cambiar_year_actualizar_ajuste_presupuestario'),
    path('cambiar_programa',cambiar_programa, name='cambiar_programa'),
]

urlpatterns += [
    path('historial_items/<uuid:id>', historial_items, name='historial_items'),
    path('modal_cdps_item_ley_presupuestaria/<uuid:item_presupuestario_id>', modal_cdps_item_ley_presupuestaria, name='modal_cdps_item_ley_presupuestaria'),
    path('modal_actualizar_cdp/<uuid:cdp_id>', modal_actualizar_cdp, name='modal_actualizar_cdp'),
]
urlpatterns += [
    path('ingresar_item_presupuestario/', ingresar_item_presupuestario, name='ingresar_item_presupuestario'),
    path('modificar_items/<int:year>', modificar_items, name='modificar_items'),
    path('modal_modificar_item/<uuid:item_presupuestario_id>', modal_modificar_item, name='modal_modificar_item'),
]

urlpatterns += [
    path('ingresar_proyeccion_inicial/<str:filter_establecimiento>', ingresar_proyeccion_inicial, name='ingresar_proyeccion_inicial'),
    path('modal_modificar_proyeccion/<uuid:mes_id>', modal_modificar_proyeccion, name='modal_modificar_proyeccion'),
]

# URL excel
urlpatterns += [
    path('export_cdps/<int:year>/<str:program>/<str:establecimiento>', exportar_cdps, name='exportar_cdps'),
    path('exportar_meses_proyectados/', exportar_meses_proyectados, name='exportar_meses_proyectados'),
    path('exportar_estimacion_subvencion/', exportar_estimacion_subvencion, name='exportar_estimacion_subvencion'),
    path('subir-archivo/', subir_archivo, name='subir_archivo'),
]



