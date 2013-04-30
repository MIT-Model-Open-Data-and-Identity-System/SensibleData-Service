from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	 url(r'^upload/', 'connectors.connector_funf.connector_funf.upload'),
	 url(r'^config/', 'connectors.connector_funf.connector_funf.config'),
)
