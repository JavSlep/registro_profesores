from django import forms
from .models import Cdp,ItemPresupuestario, FONDOS
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
import datetime
from .models import Year
from ..establecimiento.models import Establecimiento
from ..usuario.models import Unidad


class CDPFormUnidad(forms.ModelForm):
    class Meta:
        model = Cdp
        fields = '__all__'  # El campo para ingresar el código CDP
        exclude = ('created','updated','id','establecimiento','cdp','year_presupuestario')
        widgets={
            'unidad':forms.Select(attrs={'class':'form-select form-select-sm select-field'}),
            'item_presupuestario':forms.Select(attrs={'class':'form-select form-select-sm select-field'}),
            'fecha_guia_requerimiento':forms.TextInput(attrs={'class':'form-control', 'type':'date'}), 
            'fecha_cdp': forms.TextInput(attrs={'class':'form-control ', 'type':'date'}),
            'estado': forms.Select(attrs={'class': 'form-control text-uppercase'}),
        }
    def __init__(self, *args, **kwargs):
        super(CDPFormUnidad, self).__init__(*args, **kwargs)
        self.fields['item_presupuestario'].queryset = ItemPresupuestario.objects.filter(subtitulo_presupuestario__year__year=datetime.datetime.now().year,subtitulo_presupuestario__programa_presupuestario="P01 GASTOS ADMINISTRATIVOS").order_by('item')
        self.fields['fondo'].choices = [choice for choice in self.fields['fondo'].choices if choice[0] in ['APORTE FISCAL', 'OTROS']]
        self.fields['unidad'].queryset = Unidad.objects.filter().order_by('nombre')


class CDPFormEstablecimiento(forms.ModelForm):
    class Meta:
        model = Cdp
        fields = '__all__'  # El campo para ingresar el código CDP
        exclude = ('created','updated','id','unidad','cdp','year_presupuestario')
        widgets={
            'establecimiento':forms.Select(attrs={'class':'form-select form-select-sm select-field'}),
            'item_presupuestario':forms.Select(attrs={'class':'form-select form-select-sm select-field'}),
            'fecha_guia_requerimiento':forms.TextInput(attrs={'class':'form-control form-control-sm', 'type':'date'}), 
            'fecha_cdp': forms.TextInput(attrs={'class':'form-control form-control-sm', 'type':'date'}),
            'estado': forms.Select(attrs={'class': 'form-control text-uppercase'}),
        }
    def __init__(self, *args, **kwargs):
        super(CDPFormEstablecimiento, self).__init__(*args, **kwargs)
        self.fields['item_presupuestario'].queryset = ItemPresupuestario.objects.filter(subtitulo_presupuestario__year__year=datetime.datetime.now().year,subtitulo_presupuestario__programa_presupuestario="P02 SERVICIOS EDUCATIVOS").order_by('item')
        self.fields['fondo'].choices = [choice for choice in self.fields['fondo'].choices if choice[0] not in ['APORTE FISCAL', 'OTROS']]
        self.fields['establecimiento'].queryset = Establecimiento.objects.all().order_by('nombre')

