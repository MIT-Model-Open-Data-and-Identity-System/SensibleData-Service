from django.http import HttpResponse
import bson.json_util as json
from django.views.decorators.csrf import csrf_exempt
import connectors.connectors_config;

myConnector = connectors.connectors_config.CONNECTORS['ConnectorSbs2']['config']

@csrf_exempt
def upload(request):
	if request.META['CONTENT_TYPE'].split(';')[0]=='multipart/form-data':
		try:
			uploaded_file = request.FILES['uploadedfile']
			if uploaded_file:
				upload_path = myConnector['upload_path']
				if not os.path.exists(upload_path):
					os.makedirs(upload_path)
				filename = uploaded_file.name.split('.')[0].split('_')[0]+'_'+str(int(time.time()*1000))+'.raw'
				filepath = os.path.join(upload_path, filename)
				while os.path.exists(filepath):
					parts = filename.split('.raw');
					counted_parts = re.split('__',parts[0]);
					appendix = str(int(random.random()*10000))
					filename = counted_parts[0] + '__' + appendix + '.raw'
					filepath = os.path.join(upload_path, filename)
				write_file(filepath, uploaded_file)
				backup.backupFile(filepath, "connector_sbs2")
				return HttpResponse(json.dumps({'ok':'success'}))
			else: pass
		except KeyError as e: pass
	return HttpResponse(status='500')

def write_file(filepath, file):
	with open(filepath, 'wb') as output_file:
		while True:
			chunk = file.read(1024)
			if not chunk:
				break
			output_file.write(chunk)
