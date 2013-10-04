from celery import task
from questions import test_question

@task()
def add(x,y):
	return test_question.run()
