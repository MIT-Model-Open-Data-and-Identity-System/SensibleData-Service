import datetime
from django.contrib.auth.models import User
from questions.available_questions.data_quality_question import get_quality_for_users_and_period
from questions.models import QualityPrizeWinners, PrizeTicket
from sensible_audit import audit

NAME = 'quality_prize_question'
log = audit.getLogger(__name__)

def run():
	now = datetime.datetime.now()
	today = datetime.datetime(now.year, now.month, now.year)
	end_date = today - datetime.timedelta(days=1)
	start_date = end_date - datetime.timedelta(days=13)
	users = User.objects.all()
	users_to_return = [user.username for user in users if not hasattr(user, "userrole")]
	user_qualities = get_quality_for_users_and_period(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), users_to_return, 'bluetooth', 'main')
	winners = [doc for doc in user_qualities if doc['quality'] >= 0.8]

	for winner in winners:
		used_prizes = QualityPrizeWinners.objects.values_list('prize', flat=True)
		prizes = PrizeTicket.objects.order_by('?').exclude(id__in=used_prizes)
		if len(prizes) == 0:
			log.debug({"tag": "question", "type": "quality_prize", "message": "No more prizes available"})
			return

		quality_prize_winner = QualityPrizeWinners(user=winner['user'], start_timestamp=start_date, end_timestamp=end_date, quality=winner['quality'], prize=prizes[0])
		quality_prize_winner.save()
