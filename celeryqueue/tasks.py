from celery import task
from django.core.mail.message import EmailMultiAlternatives
from django.conf import settings


@task
def send_invitation_email(invitation):
    from django.template.loader import render_to_string

    originator_email = invitation.originator.user.email
    target_email = invitation.target_email
    target_name = invitation.target_name
    originator_name = invitation.originator.user.username
    signup_token = invitation.signup_token

    context = {
        'originator_email': originator_email,
        'target_email': target_email,
        'target_name': target_name,
        'originator_name': originator_name,
        'token': signup_token
    }

    message_txt = render_to_string('core/invitation_mail.txt', context)
    message_html = render_to_string('core/invitation_mail.html', context)

    message = EmailMultiAlternatives(subject="You've been invited to MBrace",
                                     body=message_txt, to=[target_email],
                                     from_email=settings.EMAIL_FROM)
    message.attach_alternative(message_html, 'text/html')

    message.send()
