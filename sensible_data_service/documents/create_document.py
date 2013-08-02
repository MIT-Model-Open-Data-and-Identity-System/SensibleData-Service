from .models import InformedConsent
import time
import get_documents
import hashlib
from utils import git_utils

def createInformedConsent(user, lang):
	InformedConsent.objects.create(user=user, accepted_at=time.time(), version=get_documents.getText('service_informed_consent_version', lang=lang), git_version=git_utils.getFileRevision(get_documents.getFilePath('service_informed_consent', lang=lang)), text_sha512=hashlib.sha512(get_documents.getText('service_informed_consent', lang=lang)).hexdigest(), lang=lang)
