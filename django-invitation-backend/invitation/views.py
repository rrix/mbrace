from __future__ import absolute_import

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.views.generic.edit import FormView

from registration.signals import user_registered
from registration.views import RegistrationView as BaseRegistrationView

from .models import InvitationError, Invitation
from .forms import InvitationForm


class RegistrationView(BaseRegistrationView):
    """Registration via invitation key."""

    def get_context_data(self, **kwargs):
        """Adds the current invitation to the context."""
        context = super(RegistrationView, self).get_context_data(**kwargs)
        context['invitation'] = self.invitation
        return context

    def get_initial(self):
        """Sets the invitation's email as the initial value for the form."""
        return {'email': self.invitation.email}

    def get_success_url(self, request, user):
        return (user.get_absolute_url(), (), {})

    def registration_allowed(self, request):
        """Search for a valid invitation key."""
        invitation_key = self.kwargs.get('invitation_key')
        try:
            self.invitation = Invitation.objects.find(invitation_key)
        except Invitation.DoesNotExist:
            return False
        return True

    def register(self, request, **cleaned_data):
        """Allow a new user to register via invitation."""
        username, email, password = cleaned_data['username'], \
                                    cleaned_data['email'], \
                                    cleaned_data['password1']
        User.objects.create_user(username, email, password)
        self.user = authenticate(username=username, password=password)
        login(request, self.user)
        user_registered.send(sender=self.__class__, user=self.user,
                             request=request)
        self.invitation.mark_accepted(self.user)
        return self.user


class InvitationView(FormView):
    """Create an invitation and send invitation email."""
    form_class = InvitationForm
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    invitation_error_url = 'invitation_unavailable'
    success_url = 'invitation_complete'
    template_name = 'invitation/invitation_form.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(InvitationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            self.invitation = Invitation.objects.invite(
                self.request.user, form.cleaned_data['email']
            )
        except InvitationError:
            return redirect(self.get_invitation_error_url())
        self.invitation.send_email()
        return redirect(self.get_success_url())

    def get_invitation_error_url(self):
        """Returns the supplied invitation_error_url."""
        if self.invitation_error_url:
            # Forcing possible reverse_lazy evaluation
            url = force_text(self.invitation_error_url)
        else:
            raise ImproperlyConfigured(
                'No url to redirect to. Provide a invitation_error_url'
            )
        return url
