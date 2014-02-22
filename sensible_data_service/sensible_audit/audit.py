
def get_request_audit_params(request):
	return {'remote_addr': request.META['REMOTE_ADDR']}