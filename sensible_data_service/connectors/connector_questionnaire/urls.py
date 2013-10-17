from django.conf.urls import patterns, include, url

urlpatterns = patterns('connectors.connector_questionnaire',
         url(r'^upload/', 'connector_questionnaire.upload'),
         url(r'^auth/grant/', 'auth.grant'),
         url(r'^auth/token/', 'auth.token'),
         url(r'^auth/refresh_token/', 'auth.refresh_token'),
#         url(r'^auth/revoke/', 'auth.revoke'),
#         url(r'^auth/sync/', 'auth.sync'),
)
