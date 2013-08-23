from django.http import HttpResponse
import json

def method(self):
    return HttpResponse(json.dumps("test"))

