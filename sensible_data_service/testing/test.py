from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from authorization_manager.authorization_manager import *
import bson.json_util as json
from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from datetime import datetime

@staff_member_required
def testing(request):
	values = {}
	values['config'] = {}
	values['config']['BASE_DIR'] = settings.BASE_DIR
	values['config']['ROOT_DIR'] = settings.ROOT_DIR
	values['config']['BASE_URL'] = settings.BASE_URL
	values['config']['ROOT_URL'] = settings.ROOT_URL


	return render_to_response("test.html", values, context_instance=RequestContext(request))

@login_required
def testing2(request):
	return HttpResponse(json.dumps(request.user.username))
