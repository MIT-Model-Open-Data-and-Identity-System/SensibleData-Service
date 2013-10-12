from datetime import timedelta

from questions import statistics_question

CELERYBEAT_SCHEDULE = {
		statistics_question.NAME: {
			'task': 'connectors.connector_answer.tasks.calculateStatistics',
			'schedule': statistics_question.SCHEDULE['schedule']
			},
		}
