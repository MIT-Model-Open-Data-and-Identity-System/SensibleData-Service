from django.core.management.base import NoArgsCommand
from utils import database
from collections import defaultdict

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		responses = defaultdict(lambda: defaultdict(dict))
		conflicts = []
		duplicates = []
		jj = 0
		db = database.Database()
		for doc in db.getDocuments(query={}, collection='dk_dtu_compute_questionnaire'):
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
