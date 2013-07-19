from .models import TosAcceptance
import time
import get_documents
import hashlib

def createTosAcceptance(user, lang):
	TosAcceptance.objects.create(user=user, accepted_at=time.time(), version=get_documents.getText('service_tos_version', lang=lang), text_sha512=hashlib.sha512(get_documents.getText('service_tos', lang=lang)).hexdigest(), lang=lang)
