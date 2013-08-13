from django.http import HttpResponse
import bson.json_util as json
from authorization_manager import authorization_manager
from utils import database
from django.shortcuts import render_to_response

def location(request):
	decrypted = booleanize(request.REQUEST.get('decrypted', False))

	if decrypted:
		return locationDecrypted(request)
	else:
		return locationEncrypted(request)






def locationDecrypted(request):
	return HttpResponse('hello decrypted')


def locationEncrypted(request):
	return HttpResponse('hello encrypted')


def booleanize(string):
	if string == False: return False
	if string == True: return True
	if string == 'True': return True
	return False
