from django.conf.urls import patterns, include, url

urlpatterns = patterns('connectors.connector_answer',
	url(r'^v1/data_stats/', 'connector_answer.data_stats'),
)
