from django.contrib import admin
from .models import *
 
class ComunaAdmin(admin.ModelAdmin):
  list_display=('id','nombre','region')
  
class RegionAdmin(admin.ModelAdmin):
  list_display=('id','nombre')

admin.site.register(Region, RegionAdmin)
admin.site.register(Comuna, ComunaAdmin)
