from django.urls import path, include
from .views import *
from .views_infraestructura import *
from .views_plan_infraestructura import *
from .views_diagnostico import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    
    
    path('establecimiento/listado_Items', login_required(listadoItems), name='listado_items'),
    path('establecimiento/listado_Items/nuevo_item', login_required(nuevoItem), name='nuevo_item'),
    path('establecimiento/listado_Items/detalle_item/<str:id_item>', login_required(detalleItem), name='detalle_item'),    
    path('establecimiento/listado_Items/editar_item/<str:id_item>', login_required(editarItem), name='editar_item'), 
    
    
    
    
    
    path('establecimiento/listado_Items/editar_item/eliminar_item_partida/<str:id_item_partida>/<str:id_item>', login_required(eliminarItemPartidaItem), name='eliminar_item_partida'),    
   
          
    
    
    
    
    path('establecimiento/listado_partidas_item', login_required(listadoPartidasItem), name='listado_partidas_item'),
    path('establecimiento/listado_partidas_item/nueva_partida_item', login_required(nuevaPartidaItem), name='nueva_partida_item'),    
    path('establecimiento/listado_partidas_item/editar_partida_item/<str:id_partida>', login_required(editarPartidaItem), name='editar_partida_item'),    
    path('establecimiento/listado_partidas_item/eliminar_partida_item/<str:id_partida>', login_required(eliminarPartidaItem), name='eliminar_partida_item'),
    
      
    path('asociar_partida_partida_mantencion/<str:id_partida>', login_required(asociarPartidaPartidaMantencion), name='asociar_partida_partidaMantencion'),
    
    path('eliminar_Partida_PartidaMantencion/<str:id_PartidaPartidaMantencion>/<str:id_partida>', login_required(eliminarPartidaPartidaMantencion), name='eliminar_Partida_PartidaMantencion'),
    
    
    
    
    path('asociar_item_partida/<str:id_partida>', login_required(asociarItemPartida), name='asociar_item_partida'),
    
    path('eliminar_item_partida/<str:id_item_partida>/<str:id_partida>', login_required(eliminarItemPartida), name='eliminar_item_partida'),
    
    
       
    
    path('establecimiento/listado_categoria_recinto', login_required(listadoCategoriaRecinto), name='listado_categoria_recinto'),    
    path('establecimiento/listado_categoria_recinto/nueva_categoria_recinto', login_required(nuevaCategoriaRecinto), name='nueva_categoria_recinto'),    
    path('establecimiento/listado_categoria_recinto/editar_categoria_recinto/<str:id_categoria_recinto> ', login_required(editarCategoriaRecinto), name='editar_categoria_recinto'),
    path('establecimiento/listado_categoria_recinto/eliminar_categoria_recinto/<str:id_categoria_recinto> ', login_required(eliminarCategoriaRecinto), name='eliminar_categoria_recinto'),
    
    
    path('establecimiento/listado_tipo_recinto', login_required(listadoTipoRecinto), name='listado_tipo_recinto'),
    path('establecimiento/listado_tipo_recinto/nuevo_tipo_recinto', login_required(nuevoTipoRecinto), name='nuevo_tipo_recinto'),    
    path('establecimiento/listado_tipo_recinto/detalle_tipo_recinto/<str:id_tipo_recinto>', login_required(detalleTipoRecinto), name='detalle_tipo_recinto'),
    
    path('establecimiento/listado_tipo_recinto/detalle_tipo_recinto/eliminar_tipo_recinto_item/<str:id_tipo_recinto_item>/<str:id_tipo_recinto>', login_required(eliminarTipoRecintoItem), name='eliminar_tipo_recinto_item'),
    
    
    
    
    path('establecimiento/listado_tipo_recinto/editar_tipo_recinto/<str:id_tipo_recinto>', login_required(editarTipoRecinto), name='editar_tipo_recinto'),
    path('establecimiento/listado_tipo_recinto/eliminar_tipo_recinto/<str:id_tipo_recinto>', login_required(eliminarTipoRecinto), name='eliminar_tipo_recinto'),
    
       
        
] 


urlpatterns += [
    
    path('establecimiento/plan_infra/resumen_plan_infraestructura/<int:year>', login_required(resumenPlanInfraestructura), name='resumen_plan_infraestructura'),
    
    
    path('establecimiento/plan_infra/nuevo_plan_infra/<str:id_establecimiento>', login_required(nuevoPlanInfra), name='nuevo_plan_infra'),
    path('establecimiento/plan_infra/instrucciones_plan_infra/<str:id_establecimiento>', login_required(instruccionesPlanInfra), name='instrucciones_plan_infra'),
    path('establecimiento/plan_infra/editar_plan_infra/<str:id_plan>/<str:id_establecimiento>', login_required(editarPlanInfra), name='editar_plan_infra'),
    
    path('establecimiento/plan_infra/detalle_plan_infra/<str:id_plan>/<str:id_establecimiento>', login_required(detallePlanInfra), name='detalle_plan_infra'), 
    
    path('modal_confirmar_envio_plan/<str:id_plan>/<str:id_establecimiento>', login_required(modalConfirmarEnvioPlan), name='modal_confirmar_envio_plan'), 
    path('cerrar_plan/<str:id_plan>/<str:id_establecimiento>', login_required(cerrarPlan), name='cerrar_plan'),    
    
    
    
    
    
    
    
    path('establecimiento/plan_infra/detalle_plan_infra/<str:id_plan>/<str:id_establecimiento>', login_required(detallePlanInfra), name='detalle_plan_infra'),
    
    path('establecimiento/plan_infra/editar_plan_infra/nuevo_pabellon/<str:id_plan>/<str:id_establecimiento>/<int:tipo_pabellon>', login_required(nuevoPabellon), name='nuevo_pabellon'),
    
    
    
    
    
        
    path('establecimiento/plan_infra/detalle_plan_infra/detalle_pabellon/<str:id_plan>/<str:id_pabellon>', login_required(detallePabellon), name='detalle_pabellon'),
    
    path('establecimiento/plan_infra/detalle_plan_infra/editar_pabellon/<str:id_plan>/<str:id_pabellon>', login_required(editarPabellon), name='editar_pabellon'),
    
    
    
    
    
    path('establecimiento/plan_infra/detalle_plan_infra/eliminar_pabellon/<str:id_plan>/<str:id_pabellon>', login_required(eliminarPabellon), name='eliminar_pabellon'),
    
    
    
    
    
    
    path('actualiza_instalacion_pabellon_htmx/<str:id_instalacion>', login_required(actualizaInstalacionPabellonHtmx), name='actualiza_instalacion_pabellon_htmx'),
    path('actualiza_instalacion_pabellon_htmx_cancel/<str:id_instalacion>', login_required(actualizaInstalacionPabellonHtmxCancel), name='actualiza_instalacion_pabellon_htmx_cancel'),
    
    
       
    
    path('establecimiento/detalle_establecimiento/planta_fisica/nuevo_recinto/<str:id_plan>/<str:id_pabellon>/<int:piso>', login_required(nuevoRecinto), name='nuevo_recinto'),
    
    path('establecimiento/detalle_establecimiento/planta_fisica/editar_recinto/<str:id_plan>/<str:id_recinto>', login_required(editarRecinto), name='editar_recinto'),
    
    
    
    
    
    path('establecimiento/detalle_establecimiento/planta_fisica/detalle_recinto/<str:id_plan>/<str:id_recinto>', login_required(detalleRecinto), name='detalle_recinto'),
    
    path('establecimiento/detalle_establecimiento/planta_fisica/eliminar_recinto/<str:id_plan>/<str:id_recinto>', login_required(eliminarRecinto), name='eliminar_recinto'),
    
    
    
    
    
    
    path('actualiza_cantidad_partida_recinto_htmx/<str:id_recinto_partida>', login_required(actualizaCantidadPartidaRencitoHtmx), name='actualiza_cantidad_partida_recinto_htmx'),
    
    path('actualiza_estado_recinto_htmx/<str:id_recinto>', login_required(actualizaEstadoRecintoHtmx), name='actualiza_estado_recinto_htmx'),
    path('actualiza_estado_recinto_htmx_cancel/<str:id_recinto>', login_required(actualizaEstadoRecintoHtmxCancel), name='actualiza_estado_recinto_htmx_cancel'),
    
    
    
    
    
] 

# URL Pabellones
urlpatterns += [
    path('actualiza_instalacion_plan_htmx/<str:id_instalacion>', actualizaInstalacionPlanHtmx, name='actualiza_instalacion_plan_htmx'),
    path('actualiza_instalacion_plan_htmx_cancel/<str:id_instalacion>', actualizaInstalacionPlanHtmxCancel, name='actualiza_instalacion_plan_htmx_cancel'),
] 


# URL Establecimiento
urlpatterns += [
    path('establecimiento/listado_establecimientos/', login_required(listadoEstablecimientos), name='listado_establecimientos'),    
    path('establecimiento/detalle_establecimiento/<str:id_establecimiento>', login_required(detalleEstablecimiento), name='detalle_establecimiento'),
    path('establecimiento/escritorio_establecimiento/<str:id_establecimiento>', login_required(escritorioEstablecimiento), name='escritorio_establecimiento'),       
] 




# URL Diagnostico
urlpatterns += [
    path('establecimiento/diagnostico/instrucciones_diagnostico/<str:id_establecimiento>', login_required(instruccionesDiagnostico), name='instrucciones_diagnostico'),
    
    path('establecimiento/diagnostico/nuevo_diagnostico/<str:id_establecimiento>', login_required(nuevoDiagnostico), name='nuevo_diagnostico'),
    path('establecimiento/diagnostico/detallle_diagnostico/<str:id_diagnostico>/<str:id_establecimiento>', login_required(detalleDiagnostico), name='detalle_diagnostico'),
    path('establecimiento/diagnostico/editar_diagnostico/<str:id_diagnostico>/<str:id_establecimiento>', login_required(editarDiagnostico), name='editar_diagnostico'),
    path('establecimiento/diagnostico/actualiza_partida_diagnostico_htmx/<str:id_partida>', login_required(actualizaPartidaDiagnosticoHtmx), name='actualiza_partida_diagnostico_htmx'),
    path('establecimiento/diagnostico/actualiza_partida_diagnostico_htmx_cancel/<str:id_partida>', login_required(actualizaPartidaDiagnosticoHtmxCancel), name='actualiza_partida_diagnostico_htmx_cancel'),
    path('establecimiento/diagnostico/modal_confirmar_envio_diagnostico/<str:id_diagnostico>/<str:id_establecimiento>', login_required(modalConfirmarEnvioDiagnostico), name='modal_confirmar_envio_diagnostico'),
    path('establecimiento/diagnostico/cerrar_diagnostico/<str:id_diagnostico>/<str:id_establecimiento>', login_required(cerrarDiagnostico), name='cerrar_diagnostico'),
    path('establecimiento/diagnostico/subir_Imagen_diagnostico', login_required(subirImagenDiagnostico), name='subir_Imagen_diagnostico'),
    path('establecimiento/diagnostico/listado_imagenes_diagnostico_htmx/<str:id_diagnostico>/', login_required(listadoImagenesDiagnosticoHtmx), name='listado_imagenes_diagnostico_htmx'),
    path('establecimiento/diagnostico/eliminar_imagen_diagnostico_htmx/<str:id_imagen>/', login_required(eliminarImagenDiagnosticoHtmx), name='eliminar_imagen_diagnostico_htmx'),    
    path('establecimiento/diagnostico/actualiza_instalacion_diagnostico_htmx/<str:id_instalacion>', login_required(actualizaInstalacionDiagnosticoHtmx), name='actualiza_instalacion_diagnostico_htmx'),
    path('establecimiento/diagnostico/actualiza_instalacion_diagnostico_htmx_cancel/<str:id_instalacion>', login_required(actualizaInstalacionDiagnosticoHtmxCancel), name='actualiza_instalacion_diagnostico_htmx_cancel'),
    
    path('establecimiento/diagnostico/actualiza_observacion_diagnostico_htmx/<str:id_diagnostico>', login_required(actualizaObservacionDiagnosticoHtmx), name='actualiza_observacion_diagnostico_htmx'),
    path('establecimiento/diagnostico/actualiza_observacion_diagnostico_htmx_cancel/<str:id_diagnostico>', login_required(actualizaObservacionDiagnosticoHtmxCancel), name='actualiza_observacion_diagnostico_htmx_cancel'),
    
        
] 



