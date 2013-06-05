from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def grant(request):

	user = request.user
	scope = request.REQUEST.get('scope').split(',')
	client_id = request.REQUEST.get('client_id')

	#TODO: create token for user for client_id
	#TODO: wrap token in authorization
	#TODO: those should be methods for different types of app exposed in authorization manager

	return HttpResponse('grant')


@login_required
def revoke(request):
	return HttpResponse(request.user)

@login_required
def sync(request):
	return HttpResponse(request.user)



def buildUri(connector, application):
	grant_uri = connector.grant_url+'?'
	revoke_uri = connector.revoke_url+'?'
	for param in application.params.all():
		if param.key == 'client_id':
			grant_uri += 'client_id='+param.value+'&'
			revoke_uri += 'client_id='+param.value+'&'
	grant_uri += 'scope=_scope_'
	revoke_uri += 'scope=_scope_'
		
	return {'grant_uri':grant_uri, 'revoke_uri': revoke_uri}
