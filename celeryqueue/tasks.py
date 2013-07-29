from celery import task
from django.core.mail import send_mail
# import core.models


@task
def send_invitation_email(invitation):
    from django.template.loader import render_to_string

    originator_email = invitation.originator.user.email
    target_email = invitation.target_email

    send_mail('Subject here', 'Here is the message.', 'from@example.com',
              ['to@example.com'], fail_silently=False)
    pass
