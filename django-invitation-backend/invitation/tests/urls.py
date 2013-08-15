from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

import invitation.urls as invitation_urls


urlpatterns = invitation_urls.urlpatterns + patterns(
    '',
    url(r'^register/$',
        TemplateView.as_view(template_name='registration/registration_register.html'),
        name='registration_register'),
    url(r'^register/complete/$',
        TemplateView.as_view(template_name='registration/registration_complete.html'),
        name='registration_complete'),
    url(r'^users/(?P<username>[\w.@+-]+)/',
        TemplateView.as_view(template_name='invitation/user_profile.html'),
        name='user_profile')
)
