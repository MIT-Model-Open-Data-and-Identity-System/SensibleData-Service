from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^accesses/daily?$', 'sensible_audit.audit.accesses'),
	url(r'^accesses/weekly?$', 'sensible_audit.audit.weekly_accesses'),
	url(r'^accesses/raw?$', 'sensible_audit.audit.raw_accesses'),
	url(r'^researchers/?$', 'sensible_audit.audit.researchers'),
	url(r'^researchers/weekly?$', 'sensible_audit.audit.weekly_researchers'),
	url(r'^researchers/requests?$', 'sensible_audit.audit.researchers_average'),
)
