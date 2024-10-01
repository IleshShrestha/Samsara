from django.conf import settings
from django.core.mail import send_mail, EmailMessage

def send_email(name, message):
    subject = name
    message = message
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["ilesh.k.shrestha@gmail.com"]

    send_mail(subject, message, from_email, recipient_list)


def send_email_attachment(name, message, image):
        subject = name
        message = message
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ["ilesh.k.shrestha@gmail.com"]
        image_url = image
        email = EmailMessage(
        f'message from {subject}',
        f'{message}', 
        f'{from_email}', 
        recipient_list)
    
        email.attach_file(image_url)
        email.send()
    