from __future__ import absolute_import

from django.contrib import admin

from .models import Invitation


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'expiration_date')
admin.site.register(Invitation, InvitationAdmin)
