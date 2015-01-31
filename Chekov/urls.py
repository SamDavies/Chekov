from django.conf.urls import patterns, include, url
from django.contrib import admin
from app import views as app_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^stops/$', app_views.stops, name='stops'),

    url(r'^admin/', include(admin.site.urls)),
)
