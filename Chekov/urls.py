from django.conf.urls import patterns, include, url
from django.contrib import admin
from bus_stop import views as app_views

urlpatterns = patterns('',

    url(r'^$', app_views.home, name='home'),

    url(r'^feed/$', app_views.live_locations, name='feed'),

    url(r'^stops/$', app_views.stops, name='stops'),

    url(r'^live_buses/$', app_views.live_locations, name='live_buses'),

    url(r'^get_feed/$', app_views.get_feed_element, name='get_feed'),

    url(r'^next_stop/$', app_views.next_stop, name='next_stop'),

    url(r'^admin/', include(admin.site.urls)),
)
