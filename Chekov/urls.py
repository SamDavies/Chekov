from django.conf.urls import patterns, include, url
from django.contrib import admin
from bus_stop import views as app_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', app_views.choose_route, name='home'),

    url(r'^stops/$', app_views.stops, name='stops'),

    url(r'^speech/$', app_views.choose_route, name='speech'),

    url(r'^admin/', include(admin.site.urls)),
)
