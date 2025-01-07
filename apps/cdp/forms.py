from django import forms
from .models import Cdp
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit


class BaseForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # Aplica la clase form-control-sm a todos los campos
    for field_name, field in self.fields.items():
      if isinstance(field.widget, forms.Select):
        # Si el campo es un select, usa las clases de select de Bootstrap 5
        field.widget.attrs.update({'class': 'form-select form-select-sm'})
      elif isinstance(field.widget, forms.Textarea):
        # Si el campo es un textarea, usa form-control-sm y define rows
        field.widget.attrs.update({'class': 'form-control form-control-sm', 'rows': '3'})          
      else:
        # Si es otro tipo de input, usa las clases de input de Bootstrap 5
        field.widget.attrs.update({'class': 'form-control form-control-sm'})       
    # Configuración opcional para agregar el helper de crispy
    self.helper = FormHelper()
    self.helper.form_show_labels = True

class CDPForm(forms.ModelForm):
    class Meta:
        model = Cdp
        fields = '__all__'  # El campo para ingresar el código CDP
        