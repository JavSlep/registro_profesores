import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
from infraslep.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from email.utils import formataddr
from email.header import Header

def emailResetPassword(email_destinatario, contexto):  
    try:
        mailServer = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)    
        mailServer.ehlo()   
        mailServer.starttls()    
        mailServer.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        mensaje = MIMEMultipart()    
        mensaje['From'] = formataddr((str(Header('InfraSLEP - Notificación', 'utf-8')), EMAIL_HOST_USER))  
        mensaje['To']=email_destinatario
        mensaje['Subject']="Cambio de Contraseña - InfraSLEP"   
        plantilla=render_to_string('email_pass.html', contexto)    
        mensaje.attach(MIMEText(plantilla, 'html'))    
        mailServer.sendmail(EMAIL_HOST_USER, email_destinatario, mensaje.as_string())   
        return True
    except Exception as e:
        print(e)
        return False