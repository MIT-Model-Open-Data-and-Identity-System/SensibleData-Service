from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from authorization_manager.authorization_manager import *
import bson.json_util as json

@login_required
def testing(request):
	response = str(request.user.username)
	return HttpResponse(response)

