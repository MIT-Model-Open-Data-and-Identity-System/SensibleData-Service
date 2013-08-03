from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	 url(r'^test/', 'testing.test.testing'),
	 url(r'^test2/', 'testing.test.testing2'),
	 
)
