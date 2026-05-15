# app/services/email_sender.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from io import BytesIO
import os

def send_email_with_attachment(to_email: str, subject: str, body: str, attachment_buffer: BytesIO, attachment_filename: str):
    """
    Envía un email con adjunto usando SMTP.
    Configurar variables de entorno: SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS
    """
    from_email = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASS")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    if not from_email or not password:
        raise ValueError("SMTP_USER y SMTP_PASS deben estar configurados")

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment_buffer.getvalue())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename={attachment_filename}")
    msg.attach(part)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()
