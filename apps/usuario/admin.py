from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'rut', 'iniciales')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
    )
    list_display=('email','first_name', 'last_name', 'is_staff')
    ordering = ('email',)
    search_fields=('first_name', 'last_name', 'email')


class UsuarioEntidadAdmin(admin.ModelAdmin):
  list_display=('usuario', 'usuario__email', 'entidad', 'establecimiento', 'cargo')
  list_filter=('entidad', 'establecimiento')  

admin.site.register(User,CustomUserAdmin)
admin.site.register(Entidad)
admin.site.register(Unidad)
admin.site.register(AreaUnidad)
admin.site.register(UsuarioEntidad, UsuarioEntidadAdmin)
