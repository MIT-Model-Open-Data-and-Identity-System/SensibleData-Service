from django.conf import settings
import os


os.system(
	"rsync --remove-source-files -azvhe ssh --exclude 'temp' " + settings.FILESYSTEM_DATABASE["LOCAL_DIR"] + " " +
	settings.FILESYSTEM_DATABASE["REMOTE_HOST"] + ":" + settings.FILESYSTEM_DATABASE["REMOTE_HOST_DIR"])
