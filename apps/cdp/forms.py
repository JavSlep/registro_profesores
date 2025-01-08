from django import forms
from .models import Cdp
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from django.contrib import messages

'''
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
    self.helper.form_show_labels = True'''

class CDPForm(forms.ModelForm):
    class Meta:
        model = Cdp
        fields = '__all__'  # El campo para ingresar el código CDP
        error_css_class = 'error'
        required_css_class = 'required'

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
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('establecimiento', css_class='form-group col-md-6 mb-0'),
                Column('unidad', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Column('item_presupuestario'),
            Row(
                Column('fondo', css_class='form-group col-md-6 mb-0'),
                Column('numero_requerimiento', css_class='form-group col-md-6 mb-0'),
            ),

            Row(                
                Column('folio_sigfe', css_class='form-group col-md-4 mb-0'),
                Column('documento', css_class='form-group col-md-4 mb-0'),
                Column('monto', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                
                
                css_class='form-row'
            ),
            'detalle',
            'otros',
            Row(
                Column('fecha_cdp', css_class='form-group col-md-6 mb-0'),
                Column('fecha_guia_requerimiento', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Guardar CDP', css_class='btn btn-success')
        )
    def clean(self):
          cleaned_data = super().clean()
          establecimiento = cleaned_data.get('establecimiento')
          unidad = cleaned_data.get('unidad')

          if (establecimiento and unidad) or (not establecimiento and not unidad):
            if establecimiento and unidad:
                raise forms.ValidationError("Debe seleccionar Establecimiento o Unidad, no ambos.")
            else:
                raise forms.ValidationError("Debe seleccionar al menos un Establecimiento o Unidad.")
          return cleaned_data 
        