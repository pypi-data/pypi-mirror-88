from celery import shared_task
from django.core.mail import EmailMessage

@shared_task()
def send_mail_task(email, subject, message):
    msg = EmailMessage(subject=subject, body=message, bcc=[email])
    msg.content_subtype = "html"
    return msg.send()