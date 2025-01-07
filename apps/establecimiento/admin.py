from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import XLSX
from django.contrib import admin
from .models import *

class EstablecimientoResources(resources.ModelResource):
    class Meta:
        model = Establecimiento
        fields = (
            'id',
            'codigo',
            'digito',
            'nombre',
            'categoria',
            'region',
            'comuna',
            'direccion',
            'zona_geografica',
            'director',
            'telefono1',
            'telefono2',
            'email_establecimiento',
            'email_director',
            'created',
            'updated',
        )     

@admin.register(Establecimiento)
class EstablecimientoAdmin(ImportExportModelAdmin):
    resource_class = EstablecimientoResources
    list_display = (        
        'codigo',
        'nombre',
        'categoria',
        'comuna',
    )

class CategoriaEstablecimientoResources(resources.ModelResource):
    class Meta:
        model = CategoriaEstablecimiento
        fields = (
            'id',            
            'nombre',
        ) 
    
    
class MatriculaResources(resources.ModelResource):
    class Meta:
        model = Matricula
        fields = (
            'id',        
            'establecimiento',
            'year',
            'matricula'
        )

class CategoriaRecintoResources(resources.ModelResource):
    class Meta:
        model = CategoriaRecinto
        fields = (
            'id',        
            'codigo',
            'nombre',
            'descripcion'            
        )
        
class TipoRecintoResources(resources.ModelResource):
    class Meta:
        model = TipoRecinto
        fields = (
            'id',        
            'codigo',
            'nombre',
            'descripcion',
            'categoria',
            'categoria_instalaciones'
        )
        


@admin.register(CategoriaEstablecimiento)
class CategoriaEstablecimientoAdmin(ImportExportModelAdmin):
    resource_class = CategoriaEstablecimientoResources
    list_display = (
        'id',        
        'nombre'
    )

@admin.register(Matricula)
class MatriculaAdmin(ImportExportModelAdmin):
    resource_class = MatriculaResources
    list_display = (
        'id',        
        'establecimiento',
        'year',
        'matricula'
    )


@admin.register(CategoriaRecinto)
class CategoriaRecintoAdmin(ImportExportModelAdmin):
    resource_class = CategoriaRecintoResources
    list_display = (
        'id',        
        'codigo',
        'nombre',
        'descripcion',
        'boolean_pabellon',
        'boolean_area'                  
    )
     
@admin.register(TipoRecinto)
class TipoRecintoAdmin(ImportExportModelAdmin):
    resource_class = TipoRecintoResources
    list_display = (
        'id',        
        'codigo',
        'nombre',
        'descripcion',
        'categoria',
    )
    list_filter=('categoria',)

class PabellonAdmin(admin.ModelAdmin):
  list_display=('nombre', 'establecimiento', 'numero_pisos')
  list_filter=('establecimiento',)

class EstadoRecintoAdmin(admin.ModelAdmin):
  list_display=('id', 'codigo', 'nombre', 'descripcion', 'class_css')
  
class ItemsAdmin(admin.ModelAdmin):
  list_display=('codigo', 'nombre', 'descripcion')  

class PlanInfraestructuraAdmin(admin.ModelAdmin):
    list_display=('establecimiento', 'establecimiento__comuna', 'year', 'estado', 'total') 

admin.site.register(EstadoRecinto, EstadoRecintoAdmin)
admin.site.register(Item, ItemsAdmin)
admin.site.register(Partida)
admin.site.register(Pabellon, PabellonAdmin)
admin.site.register(MaterialidadPabellon)
admin.site.register(Recinto)
admin.site.register(Item_Partida)
admin.site.register(PlanInfraestructura, PlanInfraestructuraAdmin)
admin.site.register(Recinto_Partida)
admin.site.register(CategoriaInstalaciones)
admin.site.register(Recinto_CategoriaInstalaciones)


class EstadoInstalacionesAdmin(admin.ModelAdmin):
  list_display=('codigo', 'nombre', 'descripcion', 'class_css')
admin.site.register(EstadoInstalaciones, EstadoInstalacionesAdmin)



admin.site.register(Plan_CategoriaInstalaciones)
admin.site.register(CategoriaPartida)
admin.site.register(TipoUnidad)
admin.site.register(Partida_PartidaMantencion)

# *********************** Diagnóstico **************************************************


class DiagnosticoAdmin(admin.ModelAdmin):
  list_display=('establecimiento', 'estado')
  
class PartidaDiagnosticoAdmin(admin.ModelAdmin):
  list_display=('nombre', 'item')
  list_filter=('item',)

class ItemDiagnosticoAdmin(admin.ModelAdmin):
  list_display=('orden', 'nombre')

admin.site.register(Diagnostico, DiagnosticoAdmin)
admin.site.register(Diagnostico_CategoriaInstalaciones)
admin.site.register(TituloItemDiagnostico)
admin.site.register(ItemDiagnostico, ItemDiagnosticoAdmin)
admin.site.register(PartidaDiagnostico, PartidaDiagnosticoAdmin)
admin.site.register(Diagnostico_PartidaDiagnostico)
admin.site.register(ImagenDiagnostico)









