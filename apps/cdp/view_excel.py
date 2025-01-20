from django.http import HttpResponse
from openpyxl import Workbook
from .models import Cdp
from openpyxl.styles import Alignment, NamedStyle, Font
from ..establecimiento.models import Establecimiento
from ..general.templatetags.utilidades import montoConPuntos
from django.shortcuts import get_object_or_404
from datetime import datetime


def exportar_cdps(request, year, program, establecimiento):
    cdps = Cdp.objects.all()
    nombre_archivo = "Reporte_cdp"
    if year != 0:
        cdps = cdps.filter(item_presupuestario__subtitulo_presupuestario__year__year=year)
        nombre_archivo += "_" + str(year)

    if program != 'todos':
        cdps = cdps.filter(item_presupuestario__subtitulo_presupuestario__programa_presupuestario=program)
        nombre_archivo += "_" + program

    if establecimiento != 'todos':
        cdps = cdps.filter(establecimiento=establecimiento)
        nombre_establecimiento = get_object_or_404(Establecimiento, id=establecimiento).nombre
        nombre_archivo += "_" + nombre_establecimiento

    # Crear un libro de trabajo y una hoja
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'CDPs'

    # Definir los encabezados
    headers = ['FECHA CDP', 'FECHA GUIA REQUERIMIENTO', 'N° REQUERIMIENTO', 'RBD', 'ESTABLECIMIENTO', 'PROGRAMA', 'FONDO', 'CUENTA CONTABLE', 'CDP', 'FOLIO SIGFE', 'N° DE ORDEN', 'MONTO', 'DETALLES', 'OTROS']
    worksheet.append(headers)

    # Aplicar formato a los encabezados
    header_style = NamedStyle(name="header_style")
    header_style.font = Font(bold=True)
    header_style.alignment = Alignment(horizontal="center", vertical="center")

    for cell in worksheet[1]:
        cell.style = header_style

    # Estilo para centrado
    centered_style = NamedStyle(name="centered")
    centered_style.alignment = Alignment(horizontal="center", vertical="center")

    cdps = cdps.order_by('cdp')
    
    # Agregar los datos a la hoja
    for cdp in cdps:
        rbd = ""
        establecimiento = ""
        if cdp.establecimiento:
            rbd = cdp.establecimiento.rbd
            establecimiento = cdp.establecimiento.nombre
        else:
            establecimiento = "SERVICIO LOCAL PUERTO CORDILLERA"
        programa = ""
        if cdp.item_presupuestario.subtitulo_presupuestario.programa_presupuestario == "P01 GASTOS ADMINISTRATIVOS":
            programa = "01"
        else:
            programa = "02"

        otros = cdp.otros if cdp.otros else "-"  # Usar una condición para manejar celdas vacías o None



        worksheet.append([
            cdp.fecha_cdp.strftime('%d/%m/%Y'),  # Listo
            cdp.fecha_guia_requerimiento.strftime('%d/%m/%Y'),  # Listo
            cdp.numero_requerimiento,  # Listo
            rbd,  # Listo
            establecimiento,  # Listo
            programa,  # Listo
            cdp.fondo,  # Listo
            cdp.item_presupuestario.concepto_presupuestario_item,  # Listo
            int(cdp.cdp),  # Listo
            cdp.folio_sigfe,  # Listo
            cdp.n_orden,  # Listo
            int(cdp.monto),  # Listo
            cdp.detalle,  # Listo
            otros,  # Listo
        ])

    # Aplicar formato a las celdas
    for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row):
        for col_idx, cell in enumerate(row, start=1):
            if col_idx == 12:  # Columna del monto
                cell.number_format = '#,##0'
                cell.alignment = centered_style.alignment
            elif col_idx == 8 or col_idx == 13 or col_idx == 14:  # Columna del concepto presupuestario
                pass
            else:
                cell.alignment = Alignment(wrap_text=True)
                cell.alignment = centered_style.alignment

    # Ajustar el ancho de las columnas según el contenido, con límite a 50
    for column_cells in worksheet.columns:
        max_length = 0
        column = column_cells[0].column_letter  # Obtener la letra de la columna
        for cell in column_cells:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
                    if max_length > 50:
                        max_length = 50
                else:
                    max_length = 10  # Si es vacío, limitar el ancho
            except:
                pass
        adjusted_width = max_length + 10  # Añadir un poco de espacio extra
        worksheet.column_dimensions[column].width = adjusted_width

    # Establecer un ancho fijo para la columna 13 (letra M y N), asegurando que no se sobrepongan
    worksheet.column_dimensions['M'].width = 50
    worksheet.column_dimensions['N'].width = 20  # Columna N más estrecha para evitar solapamiento

    fecha_actual = datetime.now().strftime('%d/%m/%Y')
    nombre_archivo += "__" + fecha_actual
    
    # Crear una respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={nombre_archivo}.xlsx'
    workbook.save(response)

    return response
