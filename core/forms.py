from django import forms
from django.contrib.localflavor.us import forms as flavorforms
from django.contrib.auth.models import User
from core.models import Hugger


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Hugger
        fields = ['name', 'phone_number', 'email', 'zip_code']


class PartialProfileForm(forms.ModelForm):
    """
    This is a fixme; I need to add some logic to disable people from changing
    their displayed username; I'm thinking that this should just pull from
    facebook, but I'd like to give someone the option to change it... once.
    Maybe that's just a support request.
    """
    class Meta:
        model = Hugger
        fields = ['name', 'phone_number', 'email', 'zip_code']


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


