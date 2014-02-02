from connectors.connector_funf.database_single_population import *
from sensible_audit import audit
import subprocess

from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		try:
			p = subprocess.Popen('ps aux | grep "manage.py database_populate" | wc -l', stdout=subprocess.PIPE, shell=True)
			out, err = p.communicate()
			try: n = (int(out.strip()) - 3)/2
			except: n = 0

			if n >= 10: return


			audit.Audit().d(type='connector_funf', tag='population', doc={'message': 'Running database population script'})
			load_files()
		except Exception as e:
			audit.Audit().e(type='connector_funf', tag='population', doc={'message': 'Exception thrown from database population script: ' + str(e)})
