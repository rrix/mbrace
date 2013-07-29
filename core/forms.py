from django import forms
from django.contrib.localflavor.us import forms as flavorforms
from django.contrib.auth.models import User
from core.models import Hugger
from gmapi.forms.widgets import GoogleMap


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
    email = forms.EmailField(required=True)

    def save(self, commit=True):
        invite = super(InviteForm, self).save(commit=False)
        invite.target_email = self.email
        if commit:
            invite.save()

        return invite
