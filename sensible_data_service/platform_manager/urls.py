from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^authorize_platform/?$', 'platform_manager.registration.authorize'),
	url(r'^redirect_uri/?$', 'platform_manager.registration.callback'),
	url(r'^informed_consent/?$', 'platform_manager.discover.informed_consent'),
	url(r'^discover/?$', 'platform_manager.discover.init'),
	url(r'^userStatus/?$', 'platform_manager.user_status.userStatus'),
	url(r'^serviceAuthorizations/?$', 'platform_manager.service_authorizations.serviceAuthorizations'),
	url(r'^logout/', 'platform_manager.logout.logout'),
)
