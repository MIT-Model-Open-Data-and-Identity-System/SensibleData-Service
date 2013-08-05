from django.conf.urls import patterns, include, url

urlpatterns = patterns('connectors.connector_facebook',

		url(r'^auth/grant_inbound/', 'auth.grantInbound'),
		url(r'^auth/granted_inbound/', 'auth.grantedInbound'),

		url(r'^auth/grant/', 'auth.grant'),
		url(r'^auth/token/', 'auth.token'),
		url(r'^auth/refresh_token/', 'auth.refresh_token'),

		#url(r'^auth/token/', 'auth.token'),
		#url(r'^auth/refresh_token/', 'auth.refresh_token'),
		#         url(r'^auth/revoke/', 'auth.revoke'),
		#         url(r'^auth/sync/', 'auth.sync'),
		)
