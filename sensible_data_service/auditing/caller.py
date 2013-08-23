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
def append(self):
    adtr = Auditor()
    returned = adtr.append("study_01", "riccardo", {"key" : "value"})
    return HttpResponse(json.dumps(returned))


def get_study_user_trail(self):
    adtr = Auditor()
    returned_list = adtr.get_study_user_trail("study_01", "riccardo")
    return HttpResponse(json.dumps(len(returned_list)))


# TODO: put the calls to the following method somewhere during the enrollment in the studies:

def user_enrollment(self):
    adtr = Auditor()
    collection_id = "study_01" + "_" "riccardo"
    key = "this_is_the_key"
    returned = adtr.user_enrollment(collection_id, key)
    return HttpResponse(json.dumps(str(returned)))

