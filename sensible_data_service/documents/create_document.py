from .models import TosAcceptance
import time
import get_documents
import hashlib
from utils import git_utils

def createTosAcceptance(user, lang):
	TosAcceptance.objects.create(user=user, accepted_at=time.time(), version=get_documents.getText('service_tos_version', lang=lang), git_version=git_utils.getFileRevision(get_documents.getFilePath('service_tos', lang=lang)), text_sha512=hashlib.sha512(get_documents.getText('service_tos', lang=lang)).hexdigest(), lang=lang)
