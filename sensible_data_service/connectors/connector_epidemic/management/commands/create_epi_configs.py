from sensible_audit import audit
from django.core.management.base import BaseCommand
from connectors.connector_epidemic import create_epi_configs

log = audit.getLogger(__name__)


class Command(BaseCommand):
	def handle(self, *args, **options):
		create_epi_configs.create_epi_configs()

