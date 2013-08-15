from django.core.management.base import BaseCommand, CommandError
from backup.run_backup import *

class Command(BaseCommand):
	def handle(self, *args, **options):
		recover(args[0])
