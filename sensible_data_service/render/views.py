from django.shortcuts import render_to_response
from django.template import RequestContext

def changebrowser(request):
	return render_to_response('changebrowser.html', {}, context_instance=RequestContext(request))

def noscript(request):
	return render_to_response('js_disabled.html', {}, context_instance=RequestContext(request))
