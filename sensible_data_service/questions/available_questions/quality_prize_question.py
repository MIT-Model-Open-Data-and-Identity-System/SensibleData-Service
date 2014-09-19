import datetime
from django.contrib.auth.models import User
from questions.available_questions.data_quality_question import get_quality_for_users_and_period
from questions.models import QualityPrizeWinners, PrizeTicket

NAME = 'quality_prize_question'

def run():
	today = datetime.datetime.now()
	end_date = today - datetime.timedelta(days=1)
	start_date = end_date - datetime.timedelta(days=14)
	start_date.hour = 0
	start_date.minute = 0
	start_date.second = 0
	users = User.objects.all()
	users_to_return = [user.username for user in users if not hasattr(user, "userrole")]
	user_qualities = get_quality_for_users_and_period(start_date, end_date, users_to_return, 'bluetooth', 'main')
	winners = [doc for doc in user_qualities if doc['quality'] >= 0.8]

	for winner in winners:
		used_prizes = QualityPrizeWinners.objects.values('prize', flat=True)
		prize = PrizeTicket.objects.order_by('?').exclude(used_prizes)[0]
		quality_prize_winner = QualityPrizeWinners(user=winner['user'], start_date=start_date, end_date=end_date, quality=winner['quality'], prize=prize)
		quality_prize_winner.save()
