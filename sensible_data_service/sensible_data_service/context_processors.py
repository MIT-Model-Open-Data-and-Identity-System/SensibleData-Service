from sensible_data_service import settings as service_settings

def service(request):
    return {'service':{'name':service_settings.SERVICE_NAME}}
