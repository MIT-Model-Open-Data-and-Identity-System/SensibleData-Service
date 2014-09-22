from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from questions.models import QualityPrizeWinners


@login_required
def see_prizes(request):
	username = request.user.username
	winner_entries = QualityPrizeWinners.objects.filter(user=username)
	prizes = [(entry.start_timestamp.strftime("%d.%m.%Y"), entry.end_timestamp.strftime("%d.%m.%Y"), int(entry.quality * 100), entry.id, entry.prize.code if entry.claimed else "") for entry in winner_entries]
	return render_to_response("prizes.html", {"prizes": prizes, "root_url": settings.BASE_URL}, context_instance=RequestContext(request))

@login_required
def claim_prize(request):
	prize_entry_id = request.REQUEST.get("prize_entry_id", "")
	prize_entry = QualityPrizeWinners.objects.get(id=int(prize_entry_id))
	prize_entry.claimed = True
	prize_entry.save(update_fields=["claimed"])
	return HttpResponse(prize_entry.prize.code, status=200, content_type="text/plain")