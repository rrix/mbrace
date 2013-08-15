from django import forms


class InvitationForm(forms.Form):
    email = forms.EmailField()
