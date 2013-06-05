from .models import *

def getApplications():
	return Application.objects.filter().all()

def getApplicationScopes(application):
	return [scope for scope in application.scopes.all()]
