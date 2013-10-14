from sensible_data_service import settings as service_settings
import os

def service(request):
    path = os.path.abspath(os.path.join(service_settings.ROOT_DIR,"..","VERSION"))
    with open(path) as f:
        version = f.read()
    is_devel = '-devel' in version

    return {'service':{'name':service_settings.SERVICE_NAME, 'version':version, 'is_devel':is_devel}}
