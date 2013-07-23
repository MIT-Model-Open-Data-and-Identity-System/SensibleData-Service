from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import auth
from django.conf import settings

def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
		return redirect(settings.PLATFORM['platform_uri']+'accounts/logout/?')
