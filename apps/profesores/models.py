from django.db import models
import uuid
import requests
from django.core.validators import FileExtensionValidator
# Create your models here.

class TeacherUser(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    
    rut = models.CharField(max_length=12)
    password = models.CharField(max_length=10)

    updated=models.DateTimeField(auto_now=True, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)

def cargar_datos():
    url = 'https://gist.githubusercontent.com/juanbrujo/0fd2f4d126b3ce5a95a7dd1f28b3d8dd/raw/b8575eb82dce974fd2647f46819a7568278396bd/comunas-regiones.json'
    response = requests.get(url)
    data = response.json()
    regiones = data['regiones']

    # Construir opciones dinámicas para regiones y comunas
    choices_regiones = []
    choices_comunas = []
    for region in regiones:
        choices_regiones.append((region['region'], region['region']))
        for comuna in region['comunas']:
            choices_comunas.append((comuna, comuna))
    return choices_regiones, choices_comunas

REGIONES, COMUNAS = cargar_datos()
class Direccion(models.Model):
    pais = models.CharField(max_length=100, default="Chile",blank=True)
    region = models.CharField(max_length=50, choices=REGIONES, blank=True)
    comuna = models.CharField(max_length=50, choices=COMUNAS, blank=True)
    direccion = models.CharField(max_length=200)

SEXO = [
    ('', 'Seleccione un sexo'),
    ('Masculino', 'Masculino'),
    ('Femenino', 'Femenino'),
    ('Prefiero no decir', 'Prefiero no decir'),
]
def cargar_datos_fecha():
    YEAR_CHOICES = [(str(year), str(year)) for year in range(1930, 2024)]
    MONTH_CHOICES = [(str(month).zfill(2), str(month).zfill(2)) for month in range(1, 13)]
    DAY_CHOICES = [(str(day).zfill(2), str(day).zfill(2)) for day in range(1, 32)]
    return YEAR_CHOICES, MONTH_CHOICES, DAY_CHOICES

YEAR, MONTH, DAY = cargar_datos_fecha()
class FechaNacimiento(models.Model):
    year = models.CharField(verbose_name="Año", choices=YEAR, max_length=4)
    month = models.CharField(verbose_name="Mes", choices=MONTH, max_length=2)
    day = models.CharField(verbose_name="Día", choices=DAY, max_length=2)
    def __str__(self):
        return f"{self.day}-{self.month}-{self.year}"
class RegisterProfesor(models.Model):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=11, verbose_name="Teléfono")

    direccion = models.OneToOneField(Direccion, on_delete=models.CASCADE)
    fecha_nacimiento = models.OneToOneField(FechaNacimiento, on_delete=models.CASCADE,null=True, blank=True)

    nacionalidad = models.CharField(max_length=100, default="Chilena",blank=True)
    teacher_user = models.OneToOneField(TeacherUser, on_delete=models.CASCADE,null=True, blank=True)
    sexo = models.CharField(max_length=20, choices=SEXO)
    cv = models.FileField(upload_to='cv_profesores/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    foto = models.FileField(upload_to='fotos_profesores/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre + ' ' + self.apellidos