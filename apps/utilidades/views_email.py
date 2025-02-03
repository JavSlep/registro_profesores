import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
from infraslep.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, BASE_DIR
from email.utils import formataddr
from email.header import Header
from django.core.mail import EmailMessage

def enviarEmail(email_destinatario, asunto, template, contexto):  
    try:       
        mailServer = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)    
        mailServer.ehlo()   
        mailServer.starttls()        
        mailServer.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        mensaje = MIMEMultipart()    
        mensaje['From'] = formataddr((str(Header('InfraSLEP - Notificación', 'utf-8')), EMAIL_HOST_USER))  
        mensaje['To']= email_destinatario
        mensaje['Cc']= 'fvilchess@outllok.com'
        mensaje['Subject']= asunto
        plantilla=render_to_string(template, contexto)
        mensaje.attach(MIMEText(plantilla, 'html'))
        """ mailServer.fail_silently = False """    
        mailServer.sendmail(EMAIL_HOST_USER, email_destinatario, mensaje.as_string())
        mailServer.close()  
        return True
    except Exception as e:
        print(e)
        return False
    
def enviarGmail(lista_email_destinatarios, lista_email_copiados, asunto, path_adjunto, template, contexto):  
    try:
        plantilla=render_to_string(template, contexto)
        emailSender = EmailMessage (
            asunto,
            plantilla,
            formataddr((str(Header('InfraSLEP - Notificación', 'utf-8')), EMAIL_HOST_USER)),
            lista_email_destinatarios,
            cc=lista_email_copiados,                       
        )
        emailSender.content_subtype = 'html'      
        if path_adjunto:            
            path_adjunto = str(BASE_DIR) + path_adjunto
            print(os.path.exists(path_adjunto))        
            with open(path_adjunto, 'rb') as f:
                emailSender.attach('cotizacion.pdf', f.read(), 'application/pdf')        
        emailSender.send(fail_silently = False)
        return True
    except Exception as e:
        print(e)
        return False

