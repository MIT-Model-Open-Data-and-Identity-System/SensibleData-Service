from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('authorization_manager.authorization_manager',
	url(r'^create_authorization/connector_funf/?', 'connectorFunf'),
)
