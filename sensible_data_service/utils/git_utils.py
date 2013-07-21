import os


def getFileRevision(filename):
	f = os.popen('git log %s | head -1'%filename)
	try: revision = f.read().split(' ')[1].strip()
	except IndexError: return '-1'
	return revision

