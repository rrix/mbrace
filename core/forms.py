from django import forms
from django.contrib.localflavor.us import forms as flavorforms
from django.contrib.auth.models import User
from core.models import Hugger
from gmapi.forms.widgets import GoogleMap
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Hugger
        fields = ['phone_number', 'email', 'zip_code']


class PartialProfileForm(forms.ModelForm):
    """
    This is a fixme; I need to add some logic to disable people from changing
    their displayed username; I'm thinking that this should just pull from
    facebook, but I'd like to give someone the option to change it... once.
    Maybe that's just a support request.
    """
    class Meta:
        model = Hugger
        fields = ['phone_number', 'email', 'zip_code']


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


class RegistrationCustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])
