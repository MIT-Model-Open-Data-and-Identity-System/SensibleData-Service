from sensible_audit import audit
from django.core.management.base import NoArgsCommand
from connectors.connector_epidemic import calculate_epi_summary

log = audit.getLogger(__name__)


class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		calculate_epi_summary.calculate_epi_summary()

