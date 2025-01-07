from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),   
    path('', include('apps.usuario.urls')),
    path('', include('apps.establecimiento.urls')),
    path('', include('apps.general.urls')),
    path('', include('apps.mantenimiento.urls')),
    path('', include('apps.utilidades.urls')),
    path('home-funcionarios/', include('apps.cdp.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)