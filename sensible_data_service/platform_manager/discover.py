from django.http import HttpResponse
import json
from django.conf import settings
from documents import get_documents

def init(request):
	response = {}
	response['service_name'] = settings.SERVICE_NAME
	response['service_desc_short'] = get_documents.getText(name='service_desc_short', lang=request.GET.get("language")).replace('\n','')
	response['service_desc_full'] = get_documents.getText(name='service_desc_full', lang=request.GET.get("language")).replace('\n','')
	return HttpResponse(json.dumps(response))

def informed_consent(request):
	response = {}
	response['service_informed_consent'] = get_documents.getText(name='service_informed_consent', lang=request.GET.get("language")).replace('\n','')
	response['service_informed_consent_version'] = get_documents.getText(name='service_informed_consent_version', lang=request.GET.get("language")).replace('\n','')
	return HttpResponse(json.dumps(response))
