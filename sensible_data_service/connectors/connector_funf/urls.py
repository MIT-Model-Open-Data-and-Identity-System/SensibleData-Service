from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	 url(r'^upload/', 'connectors.connector_funf.connector_funf.upload'),
	 url(r'^config/', 'connectors.connector_funf.connector_funf.config'),
	 url(r'^rescue/', 'connectors.connector_funf.connector_funf.rescue'),
	
	 url(r'^auth/grant/', 'connectors.connector_funf.auth.grant'),
	 url(r'^auth/gcm/', 'connectors.connector_funf.auth.gcm'),
	 url(r'^auth/initiate_grant/', 'connectors.connector_funf.auth.initiateGrant'),
	 url(r'^auth/granted/', 'connectors.connector_funf.auth.granted', name='connector_funf_auth_granted'),
	 url(r'^auth/token/', 'connectors.connector_funf.auth.token', name='connector_funf_auth_token'),
	 url(r'^auth/refresh_token/', 'connectors.connector_funf.auth.refresh_token', name='connector_funf_auth_refresh_token'),
	 url(r'^auth/revoke/', 'connectors.connector_funf.auth.revoke'),
	 url(r'^auth/sync/', 'connectors.connector_funf.auth.sync'),
)
