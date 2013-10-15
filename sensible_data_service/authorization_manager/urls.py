from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^connector_funf/?', include('connectors.connector_funf.urls')),
	url(r'^connector_raw/?', include('connectors.connector_raw.urls')),
	url(r'^connector_questionnaire/?', include('connectors.connector_questionnaire.urls')),
	url(r'^connector_facebook/?', include('connectors.connector_facebook.urls')),
    url(r'^connector_economics/?', include('connectors.connector_economics.urls')),
	url(r'^oauth2/?', include('authorization_manager.oauth2_urls')),
)
