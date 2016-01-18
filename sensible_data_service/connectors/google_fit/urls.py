# from django.conf.urls import patterns, include, url
#
# urlpatterns = patterns('connectors.google_fit',
#
# url(r'^oauth2callback', 'views.oauth2callback'),
# url(r'^selectscopes', 'views.selectscopes'),
# url(r'^exchangetoken', 'views.exchangetoken'),
# url(r'^lookupuser', 'views.lookupuser'),
# 		)


import os
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('connectors.google_fit',
    # Example:
    (r'^$', 'views.index'),
    (r'^oauth2callback', 'views.auth_return'),

)