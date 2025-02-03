from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from .validators import validation_password

class LoginUsuarioForm(forms.Form):    
  email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com', 'id':'floatingInput', 'required':True}))  
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id':'loatingPassword','required':True,'minlength':6,'maxlength':16}))
  """ captcha = ReCaptchaField(widget=ReCaptchaV2Invisible()) """


class ResetForm(forms.Form):    
  email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required':True})) 
  captcha = ReCaptchaField(widget=ReCaptchaV2Invisible())

class RestablecerPasswordForm(forms.Form):
  # Función para validar parámetros del password1
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['password1'].validators.append(validation_password)
  password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nuevo Password', 'required':True,'minlength':6,'maxlength':16}))
  password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repita Password', 'required':True,'minlength':6,'maxlength':16}))
  captcha = ReCaptchaField(widget=ReCaptchaV2Invisible())
  # Función para validar si las constraseñas son iguales  
  def clean(self):     
    super(RestablecerPasswordForm, self).clean()
    password_1 = self.cleaned_data.get('password1')    
    password_2 = self.cleaned_data.get('password2')    
    if password_1 and password_1 != password_2:      
      self._errors['password2'] = self.error_class(['Las contraseñas deben ser iguales.'])
    return self.cleaned_data