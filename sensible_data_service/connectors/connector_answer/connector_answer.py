from django.http import HttpResponse
import json
from questions import statistics_question

def data_stats(request):
	return HttpResponse(json.dumps(statistics_question.endpoint()))
