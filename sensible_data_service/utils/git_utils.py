import os


def getFileRevision(filename):
	f = os.popen('cd %s; git log %s | head -1'%(os.path.dirname(os.path.realpath(filename)),filename))
	r = f.read()
	try: revision = r.split(' ')[1].strip()
	except IndexError: return '-1'
	return revision

