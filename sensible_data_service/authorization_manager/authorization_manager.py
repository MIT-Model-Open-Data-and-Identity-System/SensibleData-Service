from .models import *

def getAuthorization(user, scope, application):
	authorizations = Authorization.objects.filter(active=True, user=user, scope=scope, application=application)
	return authorizations
