from django.urls import path

from .views import *

urlpatterns = [
    path('login_teacher', login_teacher, name='login_teacher'),
    path('registrar_profesor', registrar_profesor, name='registrar_profesor'),
    path('modal_password', modal_password, name='modal_password'),
    path('datos_personales/<str:rut>', datos_personales, name='datos_personales'),
    path('datos_curriculares', datos_curriculares, name='datos_curriculares'),
    path('datos_experiencia', datos_experiencia, name='datos_experiencia'),
    path('datos_tecnicos', datos_tecnicos, name='datos_tecnicos'),
    path('calendario_disponibilidad', calendario_disponibilidad, name='calendario_disponibilidad'),
    path('ranking_evaluacion', ranking_evaluacion, name='ranking_evaluacion'),
    path('finalizar_form', finalizar_form, name='finalizar_form'),
]
