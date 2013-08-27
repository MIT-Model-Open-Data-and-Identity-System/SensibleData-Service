### Call examples ###

from django.http import HttpResponse
import json
from utils import NON_SECURE_CONFIG
from auditor import Auditor

def ping(request):
    return HttpResponse(json.dumps("pong"))

def pull_data(self):
    returned = self.data_db['edu_mit_media_funf_probe_builtin_BluetoothProbe'].find_one()
    return HttpResponse(json.dumps("pong"))


### This "append call" must be prepended to "utils/Database.py insert"
def append(request):
    adtr = Auditor()
    collection_id = request.GET.get("collection_id")
    returned = adtr.append(collection_id, {"key" : "value"})
    return HttpResponse(json.dumps(returned))

# TODO: put the calls to the following method somewhere during the enrollment in the studies:

#def user_enrollment(request):
#    adtr = Auditor()
#    collection_id = request.GET.get("collection_id")
#    key = request.GET.get("key")
#    returned = adtr.user_enrollment(collection_id, key)
#    return HttpResponse(json.dumps(str(returned)))

# can be called using getMaxFlowId
def verify(request):
    collection_id = request.GET.get("collection_id")
    key = request.GET.get("key")
    adtr = Auditor()
    returned = adtr.verify(collection_id, 0, 5)
    return HttpResponse(returned)

def user_enrollment(request):
    username = request.GET.get("username")
    client_id = request.GET.get("client_id")
    adtr = Auditor()
    key = adtr.user_enrollment(username, client_id)
    return HttpResponse(key)



