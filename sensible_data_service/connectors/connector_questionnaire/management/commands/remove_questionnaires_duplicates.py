from collections import defaultdict

from django.core.management.base import NoArgsCommand

from db_access.named_queries.named_queries import NAMED_QUERIES
from utils import db_wrapper


class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		responses = defaultdict(lambda: defaultdict(dict))
		conflicts = []
		duplicates = []
		jj = 0
		db = db_wrapper.DatabaseHelper()
		for doc in db.execute_named_query(NAMED_QUERIES["select_questionnaires"], None):
			jj += 1
			if not jj%1000: print jj
			try:
				if responses[doc['user']][doc['variable_name']]['response'] == doc['response']:
					duplicates.append(doc)
				else:
					conflicts.append((responses[doc['user']][doc['variable_name']], doc))
			except KeyError:
				responses[doc['user']][doc['variable_name']] = doc

		print len(duplicates), len(conflicts)
