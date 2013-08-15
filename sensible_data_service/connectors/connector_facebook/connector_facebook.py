import auth
import json
import time
import urllib2
from utils import database
from anonymizer.anonymizer import Anonymizer
from backup import backup
from accounts.models import UserRole

db = None
anonymizer = None

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
			try: collectData(user, facebook_id, facebook_scope, access_token, resource_mappings[facebook_scope])
			except KeyError: continue
			except: continue

def collectData(user, facebook_id, facebook_scope, access_token, resources):
	base_url = 'https://graph.facebook.com/'
	for resource in resources:
		url = base_url
		url += '%s/?'%str(facebook_id)
		url += 'fields=%s&'%resource
		url += 'access_token=%s'%access_token

		print url
		try: getData(url, resource, user, facebook_id)
		except: continue
		#getData(url, resource, user, facebook_id)


def getData(url, resource, user, facebook_id, depth=0):
		response = json.loads(urllib2.urlopen(url).read())
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
			getData(next, resource, user, facebook_id, next_depth)


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
	doc_id = db.insert(doc, collection=probe, roles=roles)
	print doc_id
