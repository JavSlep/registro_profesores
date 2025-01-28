from django import forms
from ..usuario.models import UsuarioEntidad

class UserCargoForm(forms.ModelForm):
    class Meta:
        model = UsuarioEntidad
        fields = '__all__'
        exclude = ('id','usuario','entidad','establecimiento','administrador','estado','created','updated',)
        widgets = {
            'password': forms.PasswordInput(),
        }