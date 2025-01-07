from django.http import HttpResponse
from openpyxl import Workbook
from .models import Subtitulo

def export_subtitulos_to_excel(request):
    # Crear un libro de trabajo y una hoja
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Subtitulos'

    # Definir los encabezados
    headers = ['ID', 'Número de Subtitulo', 'Denominación', 'Actualizado', 'Creado']
    worksheet.append(headers)

    # Obtener los datos del modelo Subtitulo
    subtitulos = Subtitulo.objects.all()

    # Agregar los datos a la hoja
    for subtitulo in subtitulos:
        updated = subtitulo.updated.replace(tzinfo=None) if subtitulo.updated else None
        created = subtitulo.created.replace(tzinfo=None) if subtitulo.created else None
        worksheet.append([
            subtitulo.id,
            subtitulo.n_subtitulo,
            subtitulo.denominacion,
            updated,
            created
        ])

    # Crear una respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=subtitulos.xlsx'
    workbook.save(response)

    return response