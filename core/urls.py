from django.conf.urls import patterns, url

from core import views

urlpatterns = patterns('',
    url(r'^$',                         views.index,           name='root'),
    url(r'^dashboard/',                views.dashboard,       name='dashboard'),
    url(r'^edit_hug/(?P<hug_id>\d+)/', views.edit_hug,        name='edit_hug'),
    url(r'^new_hug/',                  views.new_hug,         name='new_hug'),
    url(r'^profile/(?P<uid>\d+)/',     views.profile,         name='profile'),
    url(r'^update_location/',          views.update_location, name='update_location'),
)
