from django.conf.urls import patterns, include, url
from django.contrib import admin
from app import views as app_views

urlpatterns = patterns('',

    url(r'^$', app_views.proxy_locator, name='home'),

    url(r'^feed/$', app_views.feed, name='feed'),

    url(r'^stops/$', app_views.stops, name='stops'),

    url(r'^live_buses/$', app_views.feed, name='live_buses'),

    url(r'^get_feed/$', app_views.get_feed_element, name='get_feed'),

    url(r'^tracker/$', app_views.tracker, name='tracker'),

    url(r'^tracker_data/$', app_views.tracker_data, name='tracker_data'),

    url(r'^admin/', include(admin.site.urls)),
)
