#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
        (r'^missing_redirect_uri/?$',   'authorization_manager.oauth2.missing_redirect_uri'),
        (r'^authorize/?$',              'authorization_manager.oauth2.authorize'),
        (r'^token/?$',                  'oauth2app.token.handler'),
)
