from django.conf.urls import patterns, url

from core import views

urlpatterns = patterns('',
    url(r'^$',                views.index,           name='root'),
    url(r'^dashboard/',       views.dashboard,       name='dashboard'),
    url(r'^profile/',         views.profile,         name='profile'),
    url(r'^update_location/', views.update_location, name='update_location'),
)
