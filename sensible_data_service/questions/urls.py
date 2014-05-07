from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^lasse_bt_network/', 'available_questions.bt_network.answer'),
	url(r'^lasse_fb_network/', 'available_questions.fb_network.answer'),
	url(r'^lasse_fb_functional_network/', 'available_questions.fb_functional_network'),
	# url(r'^lasse_call_network/', 'user.user'),

	)
