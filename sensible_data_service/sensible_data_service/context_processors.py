from django.conf import settings
import os

def service(request):
    path = os.path.abspath(os.path.join(settings.ROOT_DIR,"..","VERSION"))
    with open(path) as f:
        version = f.read()
    is_devel = '-devel' in version

    return {'service':{'name':settings.SERVICE_NAME, 'version':version, 'is_devel':is_devel}}
