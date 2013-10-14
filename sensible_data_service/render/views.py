from django.shortcuts import render_to_response
from django.template import RequestContext
from sensible_data_service import settings as service_settings

def changebrowser(request):
	return render_to_response('changebrowser.html', {'service_name':service_settings.SERVICE_NAME}, context_instance=RequestContext(request))

def noscript(request):
	return render_to_response('js_disabled.html', {'service_name':service_settings.SERVICE_NAME}, context_instance=RequestContext(request))
