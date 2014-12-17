# coding=utf-8
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from questions.models import QualityPrizeWinners
from pytz import timezone

guide_string = """1. Du starter med at klikke på <a href="http://yousee.tv/youbio/?fromsplash&cid=youseedk_youbio_gaa-til-forsiden#fromsplash" target="_blank">dette link</a> <br\> \
				  2. Derefter, vil du blive nødt til at oprette et Youbio login hvis du ikke allerede har et. Dette gøres oppe i højre hjørne under Opret bruger.<br\> \
				  3. Herinde indtaster du dine oplysninger og trykker næste.<br\> \
				  4. Derefter trykket du næste, uden at vælge noget, fordi du vil ikke have et abonnement, men kun bruge vouchersne.<br\> \
				  5. Som næste skal man indtaste oplysninger til et betalingskort, men det bliver ikke brugt til noget, det skal man bare for at oprette et login.<br\> \
				  6. Nu er oprettelsen færdig.<br\> \
				  7. Nu kan du vælge en film, trykke lej film.<br\> \
				  8. Her vil du få 2 valgmuligheder: Tilknyt betalingskort eller Gavekode/filmbillet<br\> \
				  9. Her vælger du så gavekode, trykker forsæt og indtaster den 12-cifrede voucher kode.<br\> \
				  10. Nu kan du se film, med din voucher."""

@login_required
def see_prizes(request):
	username = request.user.username
	winner_entries = QualityPrizeWinners.objects.filter(user=username)
	prizes = [(entry.start_timestamp.astimezone(timezone("Europe/Copenhagen")).strftime("%d.%m.%Y"), entry.end_timestamp.astimezone(timezone("Europe/Copenhagen")).strftime("%d.%m.%Y"), int(entry.quality * 100), entry.id, entry.prize.code if entry.claimed else "") for entry in winner_entries]
	return render_to_response("prizes.html", {"prizes": prizes, "root_url": settings.BASE_URL, "guide_string": guide_string}, context_instance=RequestContext(request))

@login_required
def claim_prize(request):
	prize_entry_id = request.REQUEST.get("prize_entry_id", "")
	prize_entry = QualityPrizeWinners.objects.get(id=int(prize_entry_id))
	prize_entry.claimed = True
	prize_entry.save(update_fields=["claimed"])
	return HttpResponse(prize_entry.prize.code, status=200, content_type="text/plain")
