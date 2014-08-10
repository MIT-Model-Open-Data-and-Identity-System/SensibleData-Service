from sensible_audit import audit
from django.core.management.base import NoArgsCommand
from connectors.connector_epidemic import analyse_epidemic

log = audit.getLogger(__name__)


class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		analyse_epidemic.analyse_epidemic()

