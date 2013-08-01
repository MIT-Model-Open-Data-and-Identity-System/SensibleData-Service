from django.http import HttpResponse
import json
from django.conf import settings
from documents import get_documents

def init(request):
	response = {}
	response['service_name'] = settings.SERVICE_NAME
	response['service_desc_short'] = get_documents.getText(name='service_desc_short', lang='da').replace('\n','')
	response['service_desc_full'] = get_documents.getText(name='service_desc_full', lang='da').replace('\n','')
	return HttpResponse(json.dumps(response))

def tos(request):
	response = {}
	response['service_tos'] = get_documents.getText(name='service_tos', lang='da').replace('\n','')
	response['service_tos_version'] = get_documents.getText(name='service_tos_version', lang='da').replace('\n','')
	return HttpResponse(json.dumps(response))
