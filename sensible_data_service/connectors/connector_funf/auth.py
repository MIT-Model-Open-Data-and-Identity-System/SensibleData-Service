import authorization_manager
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def grant(request):

        user = request.user
        scope = request.REQUEST.get('scope').split(',')
        client_id = request.REQUEST.get('client_id', '')
        device_id = request.REQUEST.get('device_id', '')
        gcm_id = request.REQUEST.get('gcm_id', '')

        #do we know gcm_id for this user:device_id?
        #if gcm_id is provided update, if not take existing one
        #otherwise we should return error that the authorization needs to be initiated from the phone

        #push user to oauth2 grant auth site, with redirect_uri back to here (connector)
        #ask for token directly, not code



        return HttpResponse(str(user) + ' ' + str(scope) + ' ' + client_id)

@login_required
def authorizationGranted(request):
        #TODO: wrap token in authorization
        #push the token to the phone over GCM
        #get confirmation somehow?
        #redirect user back to platform
        return HttpResponse('authorization granted')

@login_required
def revoke(request):

        #TODO: remove scopes from the authorization

        return HttpResponse(request.user)

@login_required
def sync(request):

        #TODO: make the authorizations reflect the submit parameters

        return HttpResponse(request.user)

def confirm(request):
	return HttpResponse('confirmed')

def buildUri(connector, application):
        grant_uri = connector.grant_url+'?'
        revoke_uri = connector.revoke_url+'?'
        for param in application.params.all():
                if param.key == 'client_id':
                        grant_uri += 'client_id='+param.value+'&'
                        revoke_uri += 'client_id='+param.value+'&'
        grant_uri += 'scope=_scope_'
        revoke_uri += 'scope=_scope_'

        #TODO: add message for the empty uris, when the action needs to be initiated from somewhere else
        return {'grant_uri':grant_uri, 'revoke_uri': revoke_uri}
