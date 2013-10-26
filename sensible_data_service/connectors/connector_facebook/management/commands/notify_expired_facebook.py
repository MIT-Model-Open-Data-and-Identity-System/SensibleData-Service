from django.core.management.base import NoArgsCommand
from authorization_manager import authorization_manager
from authorization_manager.models import Authorization
from application_manager.models import Application, GcmRegistration
from collections import defaultdict
import json
import time
from utils import database
from application_manager import gcm_server
from connectors.connector_facebook import auth

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		user_auths = defaultdict(lambda: defaultdict(int))
		authorizations = Authorization.objects.filter(application=Application.objects.get(connector_type='facebook_in'))
		db = database.Database()
		inventory = list()
		for a in authorizations:
			user = a.user
			expires_at = json.loads(a.payload)['expires_at']
			if  expires_at > user_auths[user]['expires_at']: 
				user_auths[user]['expires_at'] = expires_at
	
		now = time.time()
		for user in user_auths:
			expired = (user_auths[user]['expires_at'] < now)
			if expired:
				#TODO: base this on connetor_type
				gcm_registrations = GcmRegistration.objects.filter(user=user, application=Application.objects.get(name='Phone Data Collector'))
				if len(gcm_registrations) == 0: continue
				if len(gcm_registrations) > 1:
					for gr in gcm_registrations:
						for d in list(db.getDocuments(query={'device_id':gr.device.device_id}, collection='device_inventory')):
							if d['end'] > now and d['user'] == user.username:
								self.sendNotification(gr.gcm_id, user)

				if len(gcm_registrations) == 1: self.sendNotification(gcm_registrations[0].gcm_id, user)


	def sendNotification(self, gcm_id, user):
		print "sending to", gcm_id, user.username
		url = auth.buildInboundAuthUrl()
		#print gcm_server.sendNotification(gcm_id, {'header': 'Facebook registration', 'text':'Please renew your Facebook SensibleDTU registration by clicking this notification.', 'url': url['url'], 'type':'url'}, '')
