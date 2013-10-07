from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	 url(r'^upload/', 'connectors.connector_sbs2.connector_sbs2.upload'),
	
	url(r'^auth/grant/', 'connectors.connector_sbs2.auth.grant'),
	url(r'^auth/gcm/', 'connectors.connector_sbs2.auth.gcm'),
	url(r'^auth/initiate_grant/', 'connectors.connector_sbs2.auth.initiateGrant'),
	url(r'^auth/granted/', 'connectors.connector_sbs2.auth.granted', name='connector_sbs2_auth_granted'),
	url(r'^auth/token/', 'connectors.connector_sbs2.auth.token', name='connector_sbs2_auth_token'),
	url(r'^auth/refresh_token/', 'connectors.connector_sbs2.auth.refresh_token', name='connector_sbs2_auth_refresh_token'),
	url(r'^auth/revoke/', 'connectors.connector_sbs2.auth.revoke'),
	url(r'^auth/sync/', 'connectors.connector_sbs2.auth.sync'),
)
