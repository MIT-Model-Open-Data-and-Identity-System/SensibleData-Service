from sensible_audit import audit
from django.core.management.base import NoArgsCommand
from connectors.connector_epidemic import users_with_new_app

log = audit.getLogger(__name__)


class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		users_with_new_app.users_with_new_app()
