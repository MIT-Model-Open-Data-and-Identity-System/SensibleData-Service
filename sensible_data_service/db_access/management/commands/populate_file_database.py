import os
from django.core.management import BaseCommand
from sensible_data_service import settings


class Command(BaseCommand):

	def handle(self, *args, **options):
		print "before rsync"
		os.system(
	"rsync --remove-source-files -aze ssh --exclude 'temp' " + settings.FILESYSTEM_DATABASE["LOCAL_DIR"] + " " +
	settings.FILESYSTEM_DATABASE["REMOTE_HOST"] + ":" + settings.FILESYSTEM_DATABASE["REMOTE_HOST_DIR"])
		print "after rsync"
