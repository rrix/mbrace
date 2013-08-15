import datetime
import hashlib
import random

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.models import Site, RequestSite
from django.db import models
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

import app_settings
import signals


class InvitationError(Exception):
    pass


class InvitationManager(models.Manager):
    def invite(self, user, email):
        """Get or create an invitation for ``email`` from ``user``.

        This method doesn't an send email. You need to call ``send_email()``
        method on returned ``Invitation`` instance.
        """
        invitation = None
        try:
            # It is possible that there is more than one invitation fitting
            # the criteria. Normally this means some older invitations are
            # expired or an email is invited consequtively.
            invitation = self.filter(user=user, email=email)[0]
            if not invitation.is_valid():
                invitation = None
        except (Invitation.DoesNotExist, IndexError):
            pass
        if invitation is None:
            key = '%s%0.16f%s%s' % (settings.SECRET_KEY, random.random(),
                                    user.email, email)
            key = hashlib.sha1(key).hexdigest()
            invitation = self.create(user=user, email=email, key=key)
        return invitation
    invite.alters_data = True

    def find(self, invitation_key):
        """Find a valid invitation for the given key or raise
        ``Invitation.DoesNotExist``.

        This function always returns a valid invitation. If an invitation is
        found but not valid it will be automatically deleted.
        """
        try:
            invitation = self.filter(key=invitation_key)[0]
        except IndexError:
            raise Invitation.DoesNotExist
        if not invitation.is_valid():
            invitation.delete()
            raise Invitation.DoesNotExist
        return invitation

    def valid(self):
        """Filter valid invitations."""
        expiration = now() - datetime.timedelta(app_settings.EXPIRE_DAYS)
        return self.get_query_set().filter(date_invited__gte=expiration)

    def invalid(self):
        """Filter invalid invitation."""
        expiration = now() - datetime.timedelta(app_settings.EXPIRE_DAYS)
        return self.get_query_set().filter(date_invited__le=expiration)

    def delete_expired_keys(self):
        """Removes expired instances of ``Invitation``.

        Invitation keys to be deleted are identified by searching for
        instances of ``Invitation`` with difference between now and
        `date_invited` date greater than ``EXPIRE_DAYS``.

        It is recommended that this method be executed regularly as
        part of your routine site maintenance; this application
        provides a custom management command which will call this
        method, accessible as ``manage.py cleanupinvitations``.
        """
        return self.invalid().delete()


class Invitation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='invitations')
    email = models.EmailField(_(u'e-mail'))
    key = models.CharField(_(u'invitation key'), max_length=40, unique=True)
    date_invited = models.DateTimeField(_(u'date invited'), default=now())

    objects = InvitationManager()

    class Meta:
        verbose_name = _(u'invitation')
        verbose_name_plural = _(u'invitations')
        ordering = ('-date_invited',)

    def __unicode__(self):
        return _('%(username)s invited %(email)s on %(date)s') % {
            'username': self.user.username,
            'email': self.email,
            'date': str(self.date_invited.date()),
        }

    @models.permalink
    def get_absolute_url(self):
        return ('invitation_register', (), {'invitation_key': self.key})

    @property
    def _expires_at(self):
        return self.date_invited + datetime.timedelta(app_settings.EXPIRE_DAYS)

    def is_valid(self):
        """Return ``True`` if the invitation is still valid, ``False``
        otherwise.
        """
        return now() < self._expires_at

    def expiration_date(self):
        """Return a ``datetime.date()`` object representing expiration date.
        """
        return self._expires_at.date()
    expiration_date.short_description = _(u'expiration date')
    expiration_date.admin_order_field = 'date_invited'

    def send_email(self, email=None, site=None, request=None):
        """Send invitation email.

        Both ``email`` and ``site`` parameters are optional. If not supplied
        instance's ``email`` field and current site will be used.

        **Templates:**

        :invitation/invitation_email_subject.txt:
            Template used to render the email subject.

            **Context:**

            :invitation: ``Invitation`` instance ``send_email`` is called on.
            :site: ``Site`` instance to be used.

        :invitation/invitation_email.txt:
            Template used to render the email body.

            **Context:**

            :invitation: ``Invitation`` instance ``send_email`` is called on.
            :expiration_days: ``INVITATION_EXPIRE_DAYS`` setting.
            :site: ``Site`` instance to be used.

        **Signals:**

        ``invitation.signals.invitation_sent`` is sent on completion.
        """
        email = email or self.email
        if site is None:
            if Site._meta.installed:
                site = Site.objects.get_current()
            elif request is not None:
                site = RequestSite(request)
        subject = render_to_string('invitation/invitation_email_subject.txt',
                                   {'invitation': self, 'site': site})
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        message = render_to_string('invitation/invitation_email.txt', {
            'invitation': self,
            'expiration_days': app_settings.EXPIRE_DAYS,
            'site': site
        })
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        signals.invitation_sent.send(sender=self)

    def mark_accepted(self, new_user):
        """Update sender's invitation statistics and delete self.

        ``invitation.signals.invitation_accepted`` is sent just before the
        instance is deleted.
        """
        signals.invitation_accepted.send(sender=self,
                                         inviting_user=self.user,
                                         new_user=new_user)
        self.delete()
    mark_accepted.alters_data = True
