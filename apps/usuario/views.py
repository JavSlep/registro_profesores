import jwt
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .forms import LoginUsuarioForm
from .models import User, UsuarioEntidad, Entidad
from ..establecimiento.models import Establecimiento
from .forms import LoginUsuarioForm, RestablecerPasswordForm, ResetForm
from ..general.views_email import emailResetPassword
from datetime import datetime, timedelta
from infraslep.settings import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS, URL_DOMINIO
from django.core.serializers import serialize
import json
import datetime

def loginUsuario(request):
  form = LoginUsuarioForm(None)  
  try:    
    if request.method == 'POST':      
      form = LoginUsuarioForm(request.POST)
      if form.is_valid():        
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']             
        user = authenticate(request, email=email, password=password)  
        if user is not None:          
          login(request, user)          
          usuario_entidad = UsuarioEntidad.objects.filter(estado = True, usuario=request.user.id)            
          if usuario_entidad.count() == 1:            
            id_entidad = usuario_entidad.first().entidad.id
            usuario_entidad = UsuarioEntidad.objects.filter(usuario=request.user.id, entidad=id_entidad).first()            
            request.session['usuario_entidad'] =  {
              'year': datetime.datetime.now().year,
              'usuario': usuario_entidad.usuario.nombre_completo,
              'email': usuario_entidad.usuario.email,
              'cargo':usuario_entidad.cargo,
              'id': usuario_entidad.id,
              'administrador':usuario_entidad.administrador,
            }
            if usuario_entidad.establecimiento:
              request.session['establecimiento'] =  {
                'id': usuario_entidad.establecimiento.id,
                'nombre': usuario_entidad.establecimiento.nombre,
                'rbd': usuario_entidad.establecimiento.codigo,
              }
              return redirect('escritorio_establecimiento', usuario_entidad.establecimiento.id)
            elif usuario_entidad.area_unidad:
              request.session['area_unidad'] =  {
                'id': usuario_entidad.area_unidad.id,
                'nombre': usuario_entidad.area_unidad.nombre,
              }
              if usuario_entidad.area_unidad.unidad:
                request.session['unidad'] =  {
                  'id': usuario_entidad.area_unidad.unidad.id,
                  'nombre': usuario_entidad.area_unidad.unidad.nombre,
                }             
              return redirect('home_funcionarios',programa='none')
            else:
              return redirect('index')
          else:            
            return redirect('mis_entidades')
        else:               
          messages.error(request, 'Email o Contraseña no valida')              
  except Exception as e:
    print(e)       
    messages.error(request, 'Error inesperado')   
  return render(request, 'login_usuario.html', {'form':form})


def encoded_reset_token(user_id):  
  payload = {'user_id': user_id, 'exp': datetime.now() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)}
  encoded_data = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
  return  encoded_data

def decode_reset_token(reset_token):
  try:
    decoded_data = jwt.decode(reset_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
  except (jwt.DecodeError, jwt.ExpiredSignatureError):
    return None  # means expired token
  return decoded_data['user_id']

def passwordResetForm(request):
  form = ResetForm(None)  
  try:    
    if request.method == 'POST':         
      form = ResetForm(request.POST)
      if form.is_valid():
        email = form.cleaned_data['email']            
        try:        
          usuario = User.objects.get(email=email)                     
          email = usuario.email
          token = encoded_reset_token(usuario.password)
          contexto_email = {'url_dominio':URL_DOMINIO, 'email':email, 'token':token, 'nombres':usuario.first_name, 'apellidos':usuario.last_name}
          if emailResetPassword(email, contexto_email)==True:
            messages.success(request, "Email enviado exitosamente")
            return redirect('password_reset_done')
          else:
            messages.error(request, "Error al enviar correo")
        except User.DoesNotExist:
            messages.error(request, "Email ingresado no existe")
  except:    
      messages.error(request, 'Error inesperado')
  return render(request,"password_reset_form.html", {'form':form})

def passwordResetDone(request):
  return render(request,"password_reset_done.html")

def passwordResetConfirm(request,email,token):
  form = RestablecerPasswordForm(None)
  try:  
    if request.method == 'POST':
      form = RestablecerPasswordForm(request.POST)      
      if form.is_valid():                
        nuevo_password = form.cleaned_data['password1']
        user = User.objects.get(email=email)
        user.password = make_password(nuevo_password)
        user.save()
        messages.success(request, "Contraseña cambiada exitosamente") 
        return redirect('login')
      else:
        messages.error(request, _('Please correct the error below.'))
    else:      
      decodex = decode_reset_token(token)
      usuario = User.objects.get(email=email)
      if decodex != usuario.password:            
        messages.error(request, "Enlace inválido.") 
        return redirect ('token_invalido')    
  except:
    pass
  return render(request, 'password_reset_confirm.html', {'form': form})

def tokenInvalido(request):
  return render(request,"token_invalido.html")

def misEntidades(request):
  listado_usuario_entidad = UsuarioEntidad.objects.filter(estado = True, usuario=request.user.id)
  contexto = {'listado_usuario_entidad': listado_usuario_entidad }
  return render (request, 'mis_entidades.html', contexto)
  
def seleccionEntidad(request, id_entidad):
  usuario_entidad = UsuarioEntidad.objects.filter(usuario=request.user.id, entidad=id_entidad).first()            
  request.session['usuario_entidad'] =  {
    'usuario': usuario_entidad.usuario.nombre_completo,
    'email': usuario_entidad.usuario.email,
    'cargo':usuario_entidad.cargo,
    'id': usuario_entidad.id,
    'administrador':usuario_entidad.administrador,
  }
  if usuario_entidad.establecimiento:
    request.session['establecimiento'] =  {
      'id': usuario_entidad.establecimiento.id,
      'nombre': usuario_entidad.establecimiento.nombre,
      'rbd': usuario_entidad.establecimiento.codigo,
    }
    return redirect('escritorio_establecimiento', usuario_entidad.establecimiento.id)
  else:
    return redirect('resumen_plan_infraestructura', 2025)

