from django.conf.urls import patterns, include, url

urlpatterns = patterns('connectors.connector_raw',
	url(r'^v1/location/', 'phone_data.location'),
	url(r'^v1/wifi/', 'phone_data.wifi'),
	url(r'^v1/user/', 'user.user'),
	url(r'^v1/bluetooth/', 'phone_data.bluetooth'),
	url(r'^v1/calllog/','phone_data.calllog'),
	url(r'^v1/sms/','phone_data.sms'),
	url(r'^v1/facebook/likes/','facebook_data.likes'),
	url(r'^v1/questionnaire/', 'questionnaire.questionnaire'),

	url(r'^v1/auth/grant/', 'auth.grant'),
	url(r'^v1/auth/token/', 'auth.token'),
	url(r'^v1/auth/refresh_token/', 'auth.refresh_token'),
	url(r'^v1/auth/grant_mobile/', 'auth.grant_mobile'),
	url(r'^v1/auth/token_mobile/', 'auth.token_mobile'),
	url(r'^v1/auth/refresh_token_mobile/', 'auth.refresh_token_mobile'),
	url(r'^v1/auth/granted_mobile/', 'auth.granted_mobile'),
	url(r'^v1/auth/gcm/', 'auth.gcm'),



#         url(r'^auth/revoke/', 'auth.revoke'),
#         url(r'^auth/sync/', 'auth.sync'),
		)
