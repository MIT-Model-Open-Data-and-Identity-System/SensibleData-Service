from datetime import timedelta

from questions import test_question

CELERYBEAT_SCHEDULE = {
		'test_question': {
			'task': 'connectors.connector_answer.tasks.add',
			'schedule': test_question.SCHEDULE['schedule'],
			'args': test_question.SCHEDULE['args']
			},
		}
