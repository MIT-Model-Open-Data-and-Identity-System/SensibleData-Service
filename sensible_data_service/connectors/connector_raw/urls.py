from django.conf.urls import patterns, include, url

urlpatterns = patterns('connectors.connector_raw',
         url(r'^v1/location/', 'location.location'),
         url(r'^v1/questionnaire/', 'questionnaire.questionnaire'),

         url(r'^v1/auth/grant/', 'auth.grant'),
         url(r'^v1/auth/token/', 'auth.token'),
         url(r'^v/1auth/refresh_token/', 'auth.refresh_token'),
#         url(r'^auth/revoke/', 'auth.revoke'),
#         url(r'^auth/sync/', 'auth.sync'),
)
