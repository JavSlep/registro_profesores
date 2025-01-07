from django.urls import path
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [    
    path('accounts/login/',loginUsuario, name="login"),
    path('logout/',logout_then_login, name="logout"),    
    path('password_reset_form/',passwordResetForm, name="password_reset_form"),
    path('password_reset_done/',passwordResetDone, name="password_reset_done"),
    path('password_reset_confirm/<email>/<token>',passwordResetConfirm, name="password_reset_confirm"),
    path('token_invalido',tokenInvalido, name="token_invalido"),    
    path('',login_required(misEntidades), name="mis_entidades"),
    path('seleccion_entidad/<str:id_entidad>',login_required(seleccionEntidad), name="seleccion_entidad"),    
    
]


