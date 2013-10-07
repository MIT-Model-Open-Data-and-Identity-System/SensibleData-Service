from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	 url(r'^connector_raw/?', include('connectors.connector_raw.urls')),
	 url(r'^connector_funf/?', include('connectors.connector_funf.urls')),
	 url(r'^connector_questionnaire/?', include('connectors.connector_questionnaire.urls')),
	 url(r'^connector_facebook/?', include('connectors.connector_facebook.urls')),
	 url(r'^connector_sbs2/?', include('connectors.connector_sbs2.urls')),
)
