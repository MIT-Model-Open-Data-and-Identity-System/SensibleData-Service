from celery import task
from django.core.cache import cache
import time


@task()
def run(question, LOCK_EXPIRE=60*60):
	exec('from questions.available_questions import ' + question) in globals()
	question = eval(question)
	lock_id = 'lock-%s'%question.NAME
	acquire_lock = lambda: cache.add(lock_id, "true", LOCK_EXPIRE)
	release_lock = lambda: cache.delete(lock_id)
	print question.NAME
	if acquire_lock():
		try:
			question.run()
		finally:
			release_lock()
		return True
	return False
