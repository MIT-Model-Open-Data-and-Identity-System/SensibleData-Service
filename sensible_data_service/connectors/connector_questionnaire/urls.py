from django.conf.urls import patterns, include, url

urlpatterns = patterns('connectors.connector_questionnaire',
         #url(r'^upload/', 'connectors.connector_funf.connector_funf.upload'),

         url(r'^auth/grant/', 'auth.grant'),
#         url(r'^auth/granted/', 'auth.granted'),
#         url(r'^auth/revoke/', 'auth.revoke'),
#         url(r'^auth/sync/', 'auth.sync'),
#         url(r'^auth/confirm/', 'auth.confirm'),
)
