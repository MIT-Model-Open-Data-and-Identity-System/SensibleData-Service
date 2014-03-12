import auth
import json
import time
import urllib2
from utils import database
from anonymizer.anonymizer import Anonymizer
from backup import backup
from accounts.models import UserRole
from sensible_audit import audit
from utils import db_wrapper

db = None
anonymizer = None
ad = audit.Audit()

def collect_facebook():
	authorizations = auth.getAllInboundAuth()
	global db 
	db = database.Database()
	global anonymizer
	anonymizer = Anonymizer()

	for authorization in authorizations:
		scope = authorization.scope
		payload = json.loads(authorization.payload)
		access_token = payload['access_token']
		expires_at = payload['expires_at']
		facebook_id = payload['user_id']
		user = authorization.user
		facebook_scopes = [s.strip() for s in scope.description_extra.split('facebook: ')[1].split(',')]
		resource_mappings = auth.getResourceMappings()
		if expires_at < time.time(): continue
		for facebook_scope in facebook_scopes:
			collectData(user, facebook_id, facebook_scope, access_token, authorization, resource_mappings[facebook_scope])

def collectData(user, facebook_id, facebook_scope, access_token, authorization, resources):
	base_url = 'https://graph.facebook.com/'
	for resource in resources:
		url = base_url
		url += '%s/?'%str(facebook_id)
		url += 'fields=%s&'%resource
		url += 'access_token=%s'%access_token

		print url
		try: getData(url, resource, user, facebook_id, access_token, authorization)
		except: continue


def getData(url, resource, user, facebook_id, access_token, authorization, depth=0):
		try: response = json.loads(urllib2.urlopen(url).read())
		except urllib2.HTTPError as e:
			response = json.loads(e.read())
			if 'error' in response: 
				ad.e(type='connector_facebook', tag='get_data_error', doc={'error':response, 'user': user.username})
				if response['error']['code'] == 190:
					authorization.active = False
					authorization.save()  
				return
		
		try: data = response[resource]['data']
		except TypeError:
			try: data = response[resource] #just a string response
			except: return
		except KeyError:
			try: data = response[resource] #a single dict respnse
			except: return
		except: return
		saveData(data, resource, user, facebook_id)
		try: next = response['paging']['next']
		except KeyError: next = None
		next_depth = depth + 1
		if len(data) > 0 and next and next_depth < 6: 
			getData(next, resource, user, facebook_id, access_token, authorization, next_depth)


def saveData(data, resource, user, facebook_id):
	if len(data) == 0: return
	probe = 'dk_dtu_compute_facebook_'+resource
	facebook_id = anonymizer.anonymizeDocument(facebook_id, 'dk_dtu_compute_facebook_facebook_id')
	document = anonymizer.anonymizeDocument(data, probe)
	doc = {}
	roles = None
	try: roles = [x.role for x in UserRole.objects.get(user=user).roles.all()]
	except: pass
	doc['data'] = document
	doc['user'] = user.username
	doc['facebook_id'] = facebook_id
	doc['timestamp'] = int(time.time())
	backup.backupValue(data=doc, probe='dk_dtu_compute_facebook_'+resource, user=user.username)
	database_helper = db_wrapper.DatabaseHelper()
	doc_id = database_helper.insert(doc, collection=probe, roles=roles)
	print doc_id
