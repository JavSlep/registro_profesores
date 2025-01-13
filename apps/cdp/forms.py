from django import forms
from .models import Cdp,ItemPresupuestario, FONDOS
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
import datetime
from .models import Year

class CDPForm(forms.ModelForm):
    class Meta:
        model = Cdp
        fields = '__all__'  # El campo para ingresar el código CDP
        error_css_class = 'error'
        required_css_class = 'required'
        widgets = {
            'fecha_guia_requerimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm','format:': '%Y-%m-%d'}),
        }

    def __init__(self, *args, **kwargs):
        programa = kwargs.pop('programa', None)
        super().__init__(*args, **kwargs)

        year = datetime.datetime.now().year
        #Filtrar datos
        if programa == 'P01 GASTOS ADMINISTRATIVOS':
            self.fields['item_presupuestario'].queryset = ItemPresupuestario.objects.filter(subtitulo_presupuestario__year__year=year,subtitulo_presupuestario__programa_presupuestario='P01 GASTOS ADMINISTRATIVOS')
            # Filtrar los fondos para incluir solo "aporte fiscal"
            self.fields['fondo'].choices = [choice for choice in self.fields['fondo'].choices if choice[0] == 'APORTE FISCAL' or choice[0] =='OTROS']   
        elif programa == 'P02 SERVICIOS EDUCATIVOS':
            self.fields['item_presupuestario'].queryset = ItemPresupuestario.objects.filter(subtitulo_presupuestario__year__year=year,subtitulo_presupuestario__programa_presupuestario='P02 SERVICIOS EDUCATIVOS')
            self.fields['fondo'].choices = [choice for choice in self.fields['fondo'].choices if choice[0] not in ['APORTE FISCAL', 'OTROS']]
        

        
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
        
        try:
            current_year = Year.objects.get(year=year)
        except Year.DoesNotExist:
            print("Que pasa si no existe el año")
            fecha_cdp = datetime.date(year-1, 12, 31)
            self.fields['fecha_cdp'].initial = fecha_cdp
            self.fields['fecha_cdp'].widget.attrs['value'] = fecha_cdp.strftime('%d/%m/%Y')

        # Hacer que el campo fecha_cdp sea de solo lectura
        self.fields['fecha_cdp'].widget.attrs['readonly'] = True


        # Configuración opcional para agregar el helper de crispy
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        if programa == None:
            self.helper.layout = Layout(
                HTML('<div class="alert alert-warning" role="alert">Por favor, seleccione un programa válido.</div>')
            )
        elif programa == 'P01 GASTOS ADMINISTRATIVOS':
            self.helper.layout = Layout(
                Row(
                    Column('unidad', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'
                ),
                Column('item_presupuestario'),
                Row(
                    Column('fondo', css_class='form-group col-md-6 mb-0'),
                    Column('numero_requerimiento', css_class='form-group col-md-6 mb-0'),
                ),

                Row(                
                    Column('folio_sigfe', css_class='form-group col-md-4 mb-0'),
                    Column('n_orden', css_class='form-group col-md-4 mb-0'),
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
                Submit('submit', 'Ingresar CDP', css_class='btn btn-thick btn-thick-celeste')
            )
        elif programa == 'P02 SERVICIOS EDUCATIVOS':
            self.helper.layout = Layout(
                Row(
                    Column('establecimiento', css_class='select-field form-group col-md-12 mb-0 '),
                    css_class='form-row'
                ),
                Column('item_presupuestario'),
                Row(
                    Column('fondo', css_class='form-group col-md-6 mb-0'),
                    Column('numero_requerimiento', css_class='form-group col-md-6 mb-0'),
                ),

                Row(                
                    Column('folio_sigfe', css_class='form-group col-md-4 mb-0'),
                    Column('n_orden', css_class='form-group col-md-4 mb-0'),
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
                Submit('submit', 'Ingresar CDP', css_class='btn btn-thick btn-thick-celeste') 
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
        