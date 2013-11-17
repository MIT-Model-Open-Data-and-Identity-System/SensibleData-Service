from django.http import HttpResponse
import json
from django.conf import settings
from documents import get_documents

def init(request):
	lang = request.GET.get("language", "da")
	response = {}
	response['service_name'] = settings.SERVICE_NAME
	response['service_desc_short'] = get_documents.getText(name='service_desc_short', lang=lang).replace('\n','')
	response['service_desc_full'] = get_documents.getText(name='service_desc_full', lang=lang).replace('\n','')
	return HttpResponse(json.dumps(response))

def informed_consent(request):
	lang = request.GET.get("language", "da")
	response = {}
	response['service_informed_consent'] = get_documents.getText(name='service_informed_consent', lang=lang).replace('\n','')
	response['service_informed_consent_version'] = get_documents.getText(name='service_informed_consent_version', lang=lang).replace('\n','')
	return HttpResponse(json.dumps(response))
