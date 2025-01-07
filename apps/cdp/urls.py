from django.urls import path, include
from .views import *
from . import view_excel
from django.contrib.auth.decorators import login_required as loguin_required



# URL Diagnostico
urlpatterns = [
    path('home/', loguin_required(cdp), name='home_funcionarios'),
    path('ingresar-cdp/', ingresar_cdp, name='ingresar_cdp'),
    path('listado/', listado, name='listado'),
    path('ejemplo', Ejemplo.as_view(), name='ejemplo'),
    path('historial_cdp/', historial_cdp, name='historial_cdp'),
    path('ley_presupuestaria/<int:year>',ley_presupuestaria, name='ley_presupuestaria'),
    path('actualizar_ley_presupuestaria/<int:year>',actualizar_ley_presupuestaria, name='actualizar_ley_presupuestaria'),
    path('generar_ley_presupuestaria',generar_ley_presupuestaria, name='generar_ley_presupuestaria'),
    path('cambiar_year',cambiar_year, name='cambiar_year'),
]

# URL excel
urlpatterns += [
    path('export_subtitulos/', view_excel.export_subtitulos_to_excel, name='export_subtitulos'),
    path('subir-archivo/', subir_archivo, name='subir_archivo'),
]



