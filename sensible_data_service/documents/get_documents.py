import os


def getText(name, lang):
	path = os.path.dirname(os.path.abspath(__file__))
	filename = path+'/'+name+'_'+lang+'.txt'
	return open(filename).read()

def getFilePath(name, lang):
	path = os.path.dirname(os.path.abspath(__file__))
	filename = path+'/'+name+'_'+lang+'.txt'
	return filename
