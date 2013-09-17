from backup.run_backup import *
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
			print run_upload_to_glacier()
