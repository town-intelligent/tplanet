import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings

def send_gmail(subject, to, cont):
    content = MIMEMultipart()
    content["subject"] = subject
    content["from"] = settings.E_MAIL_SENDER
    content["to"] = to
    content.attach(MIMEText(cont, "html"))

    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
        try:
            smtp.ehlo()
            smtp.starttls()
            smtp.login("townintelligent@gmail.com", settings.SENDER_KEY)
            smtp.send_message(content)
            print("Complete!")
            return True
        except Exception as e:
            print("Error message: ", e)
            return False
