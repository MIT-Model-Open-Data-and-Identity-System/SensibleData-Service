from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^accesses/?$', 'sensible_audit.audit.accesses'),
	url(r'^researchers/?$', 'sensible_audit.audit.researchers'),
)
