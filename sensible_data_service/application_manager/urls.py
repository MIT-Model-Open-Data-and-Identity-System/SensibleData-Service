from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('application_manager.application_manager',
	url(r'^register_resource_application/?', 'registerResourceApp'),
	url(r'^register_client_application/?', 'registerClientApp'),
)
