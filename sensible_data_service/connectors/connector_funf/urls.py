from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	 url(r'^upload/', 'connectors.connector_funf.connector_funf.upload'),
	 url(r'^config/', 'connectors.connector_funf.connector_funf.config'),
	
	 url(r'^auth/grant/', 'connectors.connector_funf.auth.grant'),
	 url(r'^auth/granted/', 'connectors.connector_funf.auth.granted'),
	 url(r'^auth/revoke/', 'connectors.connector_funf.auth.revoke'),
	 url(r'^auth/sync/', 'connectors.connector_funf.auth.sync'),
	 url(r'^auth/confirm/', 'connectors.connector_funf.auth.confirm'),
)
