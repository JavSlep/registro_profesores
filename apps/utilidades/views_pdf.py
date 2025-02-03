from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa, default
# from xhtml2pdf.default import DEFAULT_CSS
from xhtml2pdf.files import pisaFileObject
# patch background color/image bleeding into other elements
# default.DEFAULT_CSS = DEFAULT_CSS.replace("background-color: transparent;", "", 1)
# patch temporary file resolution when loading fonts

pisaFileObject.getNamedFile = lambda self: self.uri

def render_to_pdf(template, contexto={}):
    template = get_template(template)
    html  = template.render(contexto)
    result = BytesIO()    
    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)
    pdf_bytes = result.getvalue()    
    result.close()      
    if pdf:        
        return pdf_bytes
    return None

