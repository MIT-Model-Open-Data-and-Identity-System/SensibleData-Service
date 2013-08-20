from django.http import HttpResponse
import bson.json_util as json
from authorization_manager import authorization_manager
from utils import database
from django.shortcuts import render_to_response

def bluetooth(request):
	decrypted = booleanize(request.REQUEST.get('decrypted', False))

	if decrypted:
		return bluetoothDecrypted(request)
	else:
		return bluetoothEncrypted(request)






def bluetoothDecrypted(request):
	return HttpResponse('hello decrypted')


def bluetoothEncrypted(request):
	return HttpResponse('hello encrypted')


def booleanize(string):
	if string == False: return False
	if string == True: return True
	if string == 'True': return True
	return False
