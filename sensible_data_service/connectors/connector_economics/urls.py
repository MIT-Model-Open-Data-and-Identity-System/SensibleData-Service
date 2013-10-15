from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
     url(r'^answer/', 'connectors.connector_economics.connector_economics.answer'),
     url(r'^list/', 'connectors.connector_economics.connector_economics.list'),

	 url(r'^auth/grant/', 'connectors.connector_economics.auth.grant'),
	 url(r'^auth/gcm/', 'connectors.connector_economics.auth.gcm'),
	 url(r'^auth/initiate_grant/', 'connectors.connector_economics.auth.initiateGrant'),
	 url(r'^auth/granted/', 'connectors.connector_economics.auth.granted', name='connector_economics_auth_granted'),
	 url(r'^auth/token/', 'connectors.connector_economics.auth.token', name='connector_economics_auth_token'),
	 url(r'^auth/refresh_token/', 'connectors.connector_economics.auth.refresh_token', name='connector_economics_auth_refresh_token'),
	 url(r'^auth/revoke/', 'connectors.connector_economics.auth.revoke'),
	 url(r'^auth/sync/', 'connectors.connector_economics.auth.sync'),
)
