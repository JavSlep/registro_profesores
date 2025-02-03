from django import forms
from .models import *
import requests

class LoginRutForm(forms.ModelForm):
    class Meta:
        model = TeacherUser
        fields = ['rut', 'password']
        help_texts = {
            'rut':'Ingrese solamente los dígitos',
            'password':'Debe ser entre 6 a 10 caracteres',
        }
        widgets = {
            'rut': forms.TextInput(attrs={'placeholder': 'Ingrese su rut'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        }
class LoginRegisterForm(forms.ModelForm):
    confirmar_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}))

    class Meta:
        model = TeacherUser
        fields = ['rut', 'password', 'confirmar_password']
        help_texts = {
            'rut':'Ingrese solamente los dígitos',
            'password':'Debe ser entre 6 a 10 caracteres',
            'confirmar_password':'Debe ser igual a la contraseña ingresada',
        }
        widgets = {
            'rut': forms.TextInput(attrs={'placeholder': 'Ingrese su rut'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Contraseña'}), 
        }

class ProfesorForm(forms.ModelForm):
    class Meta:
        model = RegisterProfesor
        fields = '__all__'
        help_texts = {
            'cv':'Ingrese su CV en formato PDF',
            'foto':'Imagen tipo carnet'
        }
        label = {
            'cv':'Curriculum Vitae (PDF)',
            'foto':'Foto de perfil'
        }
        exclude = ('id','direccion','created','updated')
        widgets = {
            'nacionalidad': forms.TextInput(attrs={'disabled': 'disabled'}),
            'sexo': forms.Select(attrs={'class':'form-select','placeholder':'Seleccione un sexo'}),
            'telefono': forms.TextInput(attrs={'placeholder': '9 1234 5678', 'class': 'form-control', 'minlength': '9'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cv'].widget.attrs['accept']='application/pdf'
        self.fields['foto'].widget.attrs['accept']='image/*'

        if self.instance and self.instance.foto:
            self.fields['foto'].label = 'Foto de perfil (Ya subida)'
        if self.instance and self.instance.cv:
            self.fields['cv'].label = 'Curriculum Vitae (Ya subido)'
class FechaForm(forms.ModelForm):
    class Meta:
        model = FechaNacimiento
        fields = '__all__'
        widgets = {
            'year': forms.Select(attrs={'class': 'form-select select-field-rc', 'required': True}),
            'month': forms.Select(attrs={'class': 'form-select select-field-rc', 'required': True}),
            'day': forms.Select(attrs={'class': 'form-select select-field-rc', 'required': True}),
        }
class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = '__all__'
        widgets = {
            'pais': forms.TextInput(attrs={'disabled': 'disabled'}),
            'region': forms.Select(attrs={'class': 'form-select select-field-rc', 'required': True}),
            'comuna': forms.Select(attrs={'class': 'form-select select-field-rc', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
