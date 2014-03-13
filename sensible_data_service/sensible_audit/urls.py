from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^dashboard/?$', 'sensible_audit.audit.dashboard'),
	url(r'^accesses/?$', 'sensible_audit.audit.accesses'),
)
