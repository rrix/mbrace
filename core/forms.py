from django import forms
# from django.contrib.localflavor.us import forms as flavorforms
from django.contrib.auth.models import User
from core.models import Hugger, Invite
from gmapi.forms.widgets import GoogleMap

import string
import uuid


class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Hugger
        fields = ['phone_number', 'zip_code']


class UserCreateForm(forms.Form):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.hugger.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class InviteForm(forms.Form):
    name = forms.CharField(required=True, max_length=32)
    email = forms.EmailField(required=True)

    def save(self, hugger, commit=True):
        invite = Invite(originator=hugger, target_email=self['email'].data)
        invite.signup_token = string.replace(str(uuid.uuid4()), '-', '')
        invite.name = self['name'].data
        if commit:
            invite.save()

        return invite
