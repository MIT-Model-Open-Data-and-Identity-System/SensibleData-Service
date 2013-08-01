from django.http import HttpResponse
import platform_manager
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
import json
from datetime import datetime

def logout(request):
	response = {'error':'something went wrong'}
	try:
		auth = platform_manager.authenticate(request)
		if 'ok' in auth:
			token_user = auth['user']
			sessions = Session.objects.filter(expire_date__gte=datetime.now())
			for session in sessions:        
				data = session.get_decoded()
				try: user = User.objects.filter(id=data.get('_auth_user_id', None))[0]				        
				except: continue
				if token_user == user:						
					session.delete()							            
					response = {'ok':'user %s logged out'%user.username}
	except: pass

	return HttpResponse(json.dumps(response))
