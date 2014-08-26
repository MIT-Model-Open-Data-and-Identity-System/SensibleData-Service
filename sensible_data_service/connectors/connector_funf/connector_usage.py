import json
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import UserRole
from authorization_manager import authorization_manager
from questions.available_questions import dateutils
from sensible_audit import audit
from utils import db_wrapper


db = db_wrapper.DatabaseHelper()
log = audit.getLogger(__name__)

@csrf_exempt
def on_post(request):
        if request.method != 'POST':
                return HttpResponse(content='POST only', status=400)

        auth = authorization_manager.authenticate_token(request)

        if 'error' in auth or not auth.get('user'):
                return HttpResponse(content='authentication failed', status=401)

        user = auth['user']

        try:
                roles = [x.role for x in UserRole.objects.get(user=auth['user']).roles.all()]
        except:
                roles = []

        try:
                appid = request.REQUEST['appid']
                events = json.loads(request.REQUEST['events'])

                if len(events) == 0 or len(events) > 1000:
                        return HttpResponse(content='malformed request', status=400)

                rows = []
                for e in events:
                        rows.append({'appid': appid,
                                     'user': user,
                                     'timestamp': dateutils.epoch_to_mysql_string(e[0]),
                                     'event': e[1]})
        except Exception as e:
                log.error({'type': 'connector_usage', 'message': str(e)})
                return HttpResponse(content='malformed request', status=400)

        db.insert_rows(rows, 'app_usage_statistics', roles=roles)

        return HttpResponse('success')
