from celery import task
from questions import statistics_question
from django.core.cache import cache
import time

@task()
def calculateStatistics():
	question = statistics_question
	collections = question.COLLECTIONS

	LOCK_EXPIRE = question.LOCK_EXPIRE
	lock_id = 'lock-%s'%question.NAME
	acquire_lock = lambda: cache.add(lock_id, "true", LOCK_EXPIRE)
	release_lock = lambda: cache.delete(lock_id)
	if acquire_lock():
		try:
			for collection in collections: question.run(collection)
		finally:
			release_lock()
		return True
	return False
