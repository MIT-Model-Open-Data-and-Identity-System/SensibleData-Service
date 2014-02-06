from django.conf.urls import patterns, include, url

urlpatterns = patterns('connectors.connector_raw',
	url(r'^v1/location/', 'raw_data.location'),
	url(r'^v1/wifi/', 'raw_data.wifi'),
	url(r'^v1/user/', 'user.user'),
	url(r'^v1/bluetooth/', 'raw_data.bluetooth'),
	url(r'^v1/calllog/','raw_data.calllog'),
	url(r'^v1/sms/','raw_data.sms'),
	url(r'^v1/facebook/likes/','raw_data.likes'),
	url(r'^v1/facebook/friends/','raw_data.friends'),
	url(r'^v1/facebook/friendlists/','raw_data.friendlists'),
	url(r'^v1/facebook/birthday/','raw_data.birthday'),
	url(r'^v1/facebook/education/','raw_data.education'),
	url(r'^v1/facebook/groups/','raw_data.groups'),
	url(r'^v1/facebook/hometown/','raw_data.hometown'),
	url(r'^v1/facebook/interests/','raw_data.interests'),
	url(r'^v1/facebook/location/','raw_data.locationfacebook'),	
	url(r'^v1/facebook/political/','raw_data.political'),
	url(r'^v1/facebook/religion/','raw_data.religion'),
	url(r'^v1/facebook/work/','raw_data.work'),
	url(r'^v1/questionnaire/', 'raw_data.questionnaire'),

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
