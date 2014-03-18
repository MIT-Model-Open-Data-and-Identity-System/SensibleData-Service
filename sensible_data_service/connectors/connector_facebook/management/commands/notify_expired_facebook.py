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
		MIN_SENSIBLE_VERSION = 'v0.3.2.3'
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
				for gr in gcm_registrations:
					for d in list(db.getDocuments(query={'device_id':gr.device.device_id}, collection='device_inventory')):
						try: sensible_version = d['sensible_version']
						except KeyError: continue
						print sensible_version
						if d['end'] > now and d['user'] == user.username and sensible_version >= MIN_SENSIBLE_VERSION:
							self.sendNotification(gr.gcm_id, user)



	def sendNotification(self, gcm_id, user):
		url = auth.buildInboundAuthUrl()
		print "sending to", gcm_id, user, url
		print gcm_server.sendNotification(gcm_id, {'title': 'Facebook registration', 'message':'Please renew your Facebook SensibleDTU registration by clicking this notification.', 'url': url['url'], 'type':'url'}, '')
