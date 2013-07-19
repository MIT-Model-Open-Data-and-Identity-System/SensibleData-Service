from django.http import HttpResponse
import json
from django.conf import settings
from documents import get_documents

def init(request):
	response = {}
	response['service_name'] = settings.SERVICE_NAME
	response['service_desc_short'] = get_documents.getText(name='service_desc_short', lang='en').replace('\n','</br>')
	response['service_desc_full'] = get_documents.getText(name='service_desc_full', lang='en').replace('\n','</br>')
	return HttpResponse(json.dumps(response))

def tos(request):
	response = {}
	response['service_tos'] = get_documents.getText(name='service_tos', lang='en').replace('\n','</br>')
	response['service_tos_version'] = get_documents.getText(name='service_tos_version', lang='en').replace('\n','</br>')
	return HttpResponse(json.dumps(response))
