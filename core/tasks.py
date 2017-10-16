from django.core.mail import EmailMessage


def send_mail(subject, msg, frm, to, html=True):
    email_message = EmailMessage(subject=subject, body=msg, from_email=frm, to=to)
    if html:
        email_message.content_subtype = "html"
    email_message.send(fail_silently=True)
