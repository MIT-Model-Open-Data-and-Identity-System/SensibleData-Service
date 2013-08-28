### Call examples ###

from django.http import HttpResponse
import json
from utils import NON_SECURE_CONFIG
from auditor import Auditor
from utils import helper

CLIENT_ID = "sensibleDTU"
USERNAME = "riccardo"

def ping(request):
    return HttpResponse(json.dumps("pong"))

def pull_data(self):
    returned = self.data_db['edu_mit_media_funf_probe_builtin_BluetoothProbe'].find_one()
    return HttpResponse(json.dumps("pong"))


### This "append call" must be prepended to "utils/Database.py insert"
def append(request):
    adtr = Auditor()
    
    collection_id = helper.collection_format(CLIENT_ID, USERNAME)
    data = {"some key" : "some value"} 	
    returned = adtr.append(collection_id, data)
    return HttpResponse(json.dumps(returned))

# TODO: put the calls to the following method somewhere during the enrollment in the studies:

# can be called using getMaxFlowId
def verify(request):
    collection_id = helper.collection_format(CLIENT_ID, USERNAME)
    adtr = Auditor()
    returned = adtr.verify(collection_id, 1, 50)
    return HttpResponse(returned)

def user_enrollment(request):
    adtr = Auditor()
    response = adtr.user_enrollment(CLIENT_ID, USERNAME)
    return HttpResponse(response["data"])



