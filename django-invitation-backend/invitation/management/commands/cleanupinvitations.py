"""
A management command which deletes expired invitation keys from the database.

Calls ``Invitation.objects.delete_expired_keys()``, which contains the actual
logic for determining which accounts are deleted.
"""

from django.core.management.base import NoArgsCommand

from invitation.models import Invitation


class Command(NoArgsCommand):
    help = "Delete expired invitation keys from the database"

    def handle_noargs(self, **options):
        Invitation.objects.delete_expired_keys()
