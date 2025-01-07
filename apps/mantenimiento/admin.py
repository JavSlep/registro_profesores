from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *


class MontoMantenimientoResources(resources.ModelResource):
    class Meta:
        model = MontoMantenimiento
        fields = (
            'id',        
            'establecimiento',
            'year',
            'monto'
        )
@admin.register(MontoMantenimiento)
class MatriculaAdmin(ImportExportModelAdmin):
    resource_class = MontoMantenimientoResources
    list_display = (
        'establecimiento__codigo',        
        'establecimiento',
        'year',
        'monto'
    )

class CategoriaPartidasResources(resources.ModelResource):
    class Meta:
        model = CategoriaPartidas
        fields = (
            'id',
            'nombre',
            'nomina_precios'
        )
@admin.register(CategoriaPartidas)
class CategoriaPartidas(ImportExportModelAdmin):
    resource_class = CategoriaPartidasResources
    list_display = (
        'id',
        'nombre',
        'nomina_precios'
    )


class PartidaNominaResources(resources.ModelResource):
    class Meta:
        model = PartidaNomina
        fields = (
            'id',
            'codigo',
            'nomina_precios',
            'precio',
            'unidad',
            'nombre',
            'categoria', 
        )
@admin.register(PartidaNomina)
class CategoriaPartidas(ImportExportModelAdmin):
    resource_class = PartidaNominaResources
    list_display = (
        'id',
        'codigo',
        'nomina_precios',
        'precio',
        'unidad',
        'nombre',
        'categoria',
    )


admin.site.register(NominaPrecios)