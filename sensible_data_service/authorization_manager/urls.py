from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('authorization_manager',
	url(r'^grant/connector_funf/?', 'connector_funf.grant'),
	url(r'^revoke/connector_funf/?', 'connector_funf.revoke'),
	url(r'^sync/connector_funf/?', 'connector_funf.sync'),
)
