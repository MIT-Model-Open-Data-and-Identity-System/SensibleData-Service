from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings

def quit(request):
	return redirect(settings.PLATFORM['platform_uri'])
