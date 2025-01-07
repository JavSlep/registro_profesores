from django import forms
from .models import Recinto, Diagnostico, Pabellon, Item, Partida, TipoRecinto, CategoriaRecinto, Pabellon_CategoriaInstalaciones, Plan_CategoriaInstalaciones, Diagnostico_PartidaDiagnostico, Diagnostico_CategoriaInstalaciones
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



class PabellonForm(forms.ModelForm):
  class Meta:
    model = Pabellon
    fields = '__all__'
    exclude = ('codigo',)    
    widgets = {            
      'nombre':forms.TextInput(attrs={'class':'form-control form-control-sm'}),      
      'numero_pisos':forms.Select(attrs={'class':'form-select form-select-sm'}),
      'descripcion': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'3', 'placeholder':'Ingrese descripción opcional.'})
    }

class AreaExteriorForm(forms.ModelForm):
  class Meta:
    model = Pabellon
    fields = '__all__'
    exclude = ('codigo','numero_pisos')    
    widgets = {            
      'nombre':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
      'descripcion': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'3', 'placeholder':'Ingrese descripción opcional.'})
    }

class PabellonEditForm(forms.ModelForm):
  class Meta:
    model = Pabellon
    fields = ('nombre','descripcion')
    widgets = {            
      'nombre':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
      'descripcion': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'3', 'placeholder':'Ingrese descripción opcional.'})
    }
   
            
class RecintoForm(forms.ModelForm):
  class Meta:
    model = Recinto
    fields = '__all__'    
    exclude = ('superficie','estado', 'observacion_estado')
    
class EditRecintoForm(forms.ModelForm):
  class Meta:
    model = Recinto
    fields = ('nombre','descripcion')
    widgets = { 
      'nombre':forms.TextInput(attrs={'class':'form-control form-control-sm'}), 
      'descripcion': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'3', 'placeholder':'Ingrese descripción opcional.'})
    }    
        
class RecintoEstadoForm(forms.ModelForm):
  class Meta:
    model = Recinto
    fields = ('estado', 'observacion_estado')
    widgets = {
      'estado':forms.Select(attrs={'class':'form-select form-select-sm'}),      
      'observacion_estado': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'3', 'placeholder':'Ingrese observación opcional.'}),
    }   

class ItemForm(forms.ModelForm):
  class Meta:
    model = Item
    fields = '__all__'
    widgets = {            
      'codigo':forms.TextInput(attrs={'class':'form-control form-control-sm'}), 
      'nombre':forms.TextInput(attrs={'class':'form-control form-control-sm'}), 
      'descripcion': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'3', 'placeholder':'Ingrese descripción opcional.'})
    }

class PartidaForm(BaseForm):
  class Meta:
    model = Partida
    """ fields = '__all__' """
    fields = ('codigo', 'nombre', 'unidad', 'precio', 'categoria_partida', 'descripcion')
    """ labels = {
      'nombre': 'Nombre completo',
   
    } """
    widgets = {      
      'descripcion': forms.Textarea(attrs={'placeholder':'Ingrese descripción opcional.'}),             
    }
    
class EditPartidaForm(BaseForm):
  class Meta:
    model = Partida
    fields = '__all__'
    widgets = {
      
      'descripcion': forms.Textarea(attrs={'placeholder':'Ingrese descripción opcional.'}),             
    }
""" 'partida_nomina':forms.Select(attrs={'class':'form-select form-select-sm', 'id':'select-field'}), """
   
class CategoriaRecintoForm(forms.ModelForm):
  class Meta:
    model = CategoriaRecinto
    fields = '__all__'
    widgets = {
      'codigo':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
      'nombre':forms.TextInput(attrs={'class':'form-control form-control-sm'}), 
      'descripcion': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'3', 'placeholder':'Ingrese descripción opcional.'}),     
      
    }

class TipoRecintoForm(forms.ModelForm):
  class Meta:
    model = TipoRecinto
    fields = '__all__'
    exclude = ('estado',)
    widgets = {
      'codigo':forms.TextInput(attrs={'class':'form-control form-control-sm'}),
      'nombre':forms.TextInput(attrs={'class':'form-control form-control-sm'}), 
      'categoria':forms.Select(attrs={'class':'form-select form-select-sm'}),
      'categoria_instalaciones':  forms.CheckboxSelectMultiple(attrs={'class':'form-check-input', 'type':'checkbox',}),
      'descripcion': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'3', 'placeholder':'Ingrese descripción opcional.'}),      
      
    }

class Pabellon_CategoriaInstalacionesForm(forms.ModelForm):
  class Meta:
    model = Pabellon_CategoriaInstalaciones
    fields = ('estado', 'observaciones')
    widgets = {
      'estado':forms.Select(attrs={'class':'form-select form-select-sm'}),      
      'observaciones': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'3', 'placeholder':'Ingrese observación opcional.'}),
    }

class Plan_CategoriaInstalacionesForm(forms.ModelForm):
  class Meta:
    model = Plan_CategoriaInstalaciones
    fields = ('estado', 'observaciones')
    widgets = {
      'estado':forms.Select(attrs={'class':'form-select form-select-sm'}),      
      'observaciones': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'3', 'placeholder':'Ingrese observación que justifique el estado de funcionamiento ingresado.'}),
    }

class Diagnostico_PartidaDiagnosticoForm(forms.ModelForm):
  class Meta:
    model = Diagnostico_PartidaDiagnostico
    fields = ('evaluacion', 'observaciones')
    widgets = {
      'evaluacion':forms.Select(attrs={'class':'form-select form-select-sm'}),      
      'observaciones': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'3', 'placeholder':'Ingrese observación que justifique la evaluación.', 'required':True}),
    }

class Diagnostico_CategoriaInstalacionesForm(forms.ModelForm):
  class Meta:
    model = Diagnostico_CategoriaInstalaciones
    fields = ('estado', 'observaciones')
    widgets = {
      'estado':forms.Select(attrs={'class':'form-select form-select-sm'}),      
      'observaciones': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'3', 'placeholder':'Ingrese observación que justifique la evaluación.', 'required':True}),
    }

class ObservacionDiagnosticoForm(forms.ModelForm):
  class Meta:
    model = Diagnostico
    fields = ('observaciones',)
    widgets = {      
      'observaciones': forms.Textarea(attrs={'class':'form-control form-control-sm', 'rows':'3', 'placeholder':'Ingrese observación general (opcional).'}),
    }