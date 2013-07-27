#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
        url(r'^missing_redirect_uri/?$',   'authorization_manager.oauth2.missing_redirect_uri'),
        url(r'^authorize/?$',              'authorization_manager.oauth2.authorize', name='oauth2_authorize'),
        url(r'^token/?$',                  'oauth2app.token.handler'),
)
