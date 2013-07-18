import os, sys
from utils.database import Database
from anonymizer import anonymizer

class Connector(object):
	db = None
	anonymizer = None

	def __init__(self):
		self.db = Database()
		self.anonymizer = anonymizer.Anonymizer()

