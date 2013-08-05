from django.conf.urls import patterns, url

from core import views

urlpatterns = patterns('',
    url(r'^$',                                  views.index,               name='root'),
    url(r'^dashboard/',                         views.dashboard,           name='dashboard'),
    url(r'^edit_hug/(?P<hug_id>\d+)/',          views.edit_hug,            name='edit_hug'),
    url(r'^new_hug/',                           views.new_hug,             name='new_hug'),
    url(r'^profile/(?P<uid>\d+)/',              views.profile,             name='profile'),
    url(r'^update_location/',                   views.update_location,     name='update_location'),
    url(r'^new_message/(?P<hug_id>\d+)/',       views.new_message,         name='new_message'),
    url(r'^send_invite',                        views.send_invite,         name='send_invite'),
    url(r'^account_activation/(?P<token>\w+)/', views.activate_invitation, name='activate_invitation'),
)
