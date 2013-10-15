from celery import task
from django.core.cache import cache
import time

@task()
def run(question, name):
	LOCK_EXPIRE = 60*60 #max time in sec after which the task will be considered zombie
	lock_id = 'lock-%s'%name
	acquire_lock = lambda: cache.add(lock_id, "true", LOCK_EXPIRE)
	release_lock = lambda: cache.delete(lock_id)
	if acquire_lock():
		try:
			question()
		finally:
			release_lock()
		return True
	return False
