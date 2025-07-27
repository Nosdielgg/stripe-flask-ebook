import smtplib
from email.message import EmailMessage
import os

def send_ebook(recipient_email):
    msg = EmailMessage()
    msg["Subject"] = "Seu e-book chegou!"
    msg["From"] = os.environ["EMAIL_USER"]
    msg["To"] = recipient_email
    msg.set_content("Obrigado pela sua compra! Clique no link abaixo para baixar seu e-book.")

    ebook_url = "https://drive.google.com/uc?export=download&id=ID_DO_ARQUIVO"

    msg.add_alternative(f"""
    <html>
        <body>
            <p>Olá!</p>
            <p>Obrigado pela sua compra.</p>
            <p><a href="{ebook_url}">Clique aqui para baixar seu e-book</a></p>
        </body>
    </html>
    """, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
        smtp.send_message(msg)
