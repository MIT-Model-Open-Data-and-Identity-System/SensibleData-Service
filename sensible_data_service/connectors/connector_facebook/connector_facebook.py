import auth
import json
import time
import urllib2
from utils import database
from anonymzier import anonymizer

def collect_facebook():
	authorizations = auth.getAllInboundAuth()
	db = database.Database()


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
		url += '%s/'%str(facebook_id)
		url += '%s/?'%resource
		url += 'access_token=%s'%access_token

		try: getData(url, resource)
		except: continue


def getData(url, resource, depth=0):
		response = json.loads(urllib2.urlopen(url).read())
		data = response['data']
		saveData(data, resource)
		try: next = response['paging']['next']
		except KeyError: next = None
		next_depth = depth + 1
		if len(data) > 0 and next and next_depth < 3: 
			getData(next, resource, next_depth)


def saveData(data, resource):
	if len(data) == 0: return
	print resource, data
