from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

# These method have been used only for testing and debuggin. Logging would be executed with python calls among the modules, not using REST API. For now        
    url(r'^ping', "auditing.caller.ping"), # folder.module.method or app.views.view
    url(r'^append', "auditing.caller.append"),
    url(r'^pull_data', "auditing.caller.pull_data"),
 #   url(r'^get_study_user_trail', "auditing.caller.get_study_user_trail"),
 #   url(r'^set_key', "auditing.caller.set_key"),
    url(r'^user_enrollment', "auditing.caller.user_enrollment"),
    url(r'^verify', "auditing.caller.verify"),
#    url(r'^key_generation', "auditing.caller.key_generation"),
    

)
