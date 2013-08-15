from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from registration.backends.default.views import RegistrationView
from core.forms import RegistrationCustomUserForm

urlpatterns = patterns('',
    url(r'^', include('core.urls')),


    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationCustomUserForm), name='registration_register'),

    (r'^accounts/', include('registration.backends.default.urls')),
    (r'^facebook/', include('django_facebook.urls')),
    (r'^accounts/', include('django_facebook.auth_urls')),
)
