import datetime
from django.core import mail
from django.contrib.auth.models import User
from django.utils.timezone import now

from utils import BaseTestCase
from invitation import app_settings
from invitation.models import Invitation


EXPIRE_DAYS = app_settings.EXPIRE_DAYS


class InvitationTestCase(BaseTestCase):
    def setUp(self):
        super(InvitationTestCase, self).setUp()
        user = self.user()
        self.invitation = Invitation.objects.create(user=user,
                                                    email=u'test@example.com',
                                                    key=u'F' * 40)

    def make_invalid(self, invitation=None):
        invitation = invitation or self.invitation
        invitation.date_invited = now() - datetime.timedelta(EXPIRE_DAYS + 10)
        invitation.save()
        return invitation

    def test_send_email(self):
        self.invitation.send_email()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].recipients()[0], u'test@example.com')
        self.invitation.send_email(u'other@email.org')
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].recipients()[0], u'other@email.org')

    def test_mark_accepted(self):
        new_user = User.objects.create_user('test', 'test@example.com', 'test')
        pk = self.invitation.pk
        self.invitation.mark_accepted(new_user)
        self.assertRaises(Invitation.DoesNotExist,
                          Invitation.objects.get, pk=pk)

    def test_invite(self):
        Invitation.objects.all().delete()
        invitation = Invitation.objects.invite(self.user(), 'test@example.com')
        self.assertEqual(invitation.user, self.user())
        self.assertEqual(invitation.email, 'test@example.com')
        self.assertEqual(len(invitation.key), 40)
        self.assertEqual(invitation.is_valid(), True)
        self.assertEqual(type(invitation.expiration_date()), datetime.date)
        # Test if existing valid record is returned
        # when we try with the same credentials
        self.assertEqual(Invitation.objects.invite(self.user(),
                                              'test@example.com'), invitation)
        # Try with an invalid invitation
        invitation = self.make_invalid(invitation)
        new_invitation = Invitation.objects.invite(self.user(),
                                                   'test@example.com')
        self.assertEqual(new_invitation.is_valid(), True)
        self.assertNotEqual(new_invitation, invitation)

    def test_find(self):
        self.assertEqual(Invitation.objects.find(self.invitation.key),
                         self.invitation)
        invitation = self.make_invalid()
        self.assertEqual(invitation.is_valid(), False)
        self.assertRaises(Invitation.DoesNotExist,
                          Invitation.objects.find, invitation.key)
        self.assertEqual(Invitation.objects.all().count(), 0)
        self.assertRaises(Invitation.DoesNotExist,
                          Invitation.objects.find, '')
