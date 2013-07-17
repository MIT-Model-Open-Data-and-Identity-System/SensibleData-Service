from django.http import HttpResponse
from django.shortcuts import redirect
from utils import service_config


def quit(request):
	return redirect(service_config.PLATFORM['platform_uri'])
