from Crypto.Cipher import AES
from Crypto import Random
from utils import SECURE_service_config


class Anonymizer(object):

	BS = 16

	def __init__(self):
		pass
	

	def pad(self, s):
		return s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)

	def unpad(self, s):
		return s[0:-ord(s[-1])]


	def encryptDocument(self, document, probe):
		key = SECURE_service_config['PROBE_KEYS'][probe]
		self.key = key.decode("hex")
		#to throught the document and find fields that should be encrypted; put this in the config
		for key in document:
			pass

	def encrypt(self, raw):
		raw = self.pad(raw)
		#we use fixed iv to have consistent encryption
		iv =  '1234567812345678'
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return (iv + cipher.encrypt(raw)).encode("hex")

	def decrypt(self, enc):
		enc = enc.decode("hex")
		iv = enc[:16]
		enc = enc[16:]
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return self.unpad(cipher.decrypt(enc))
		


anonymizer = Anonymizer("140b41b22a29beb4061bda66b6747e14")
ciphertext = anonymizer.encrypt("Hello worldfdsfdsfsafdsfasdfsdfsdfdsfsdfds")
plain = anonymizer.decrypt(ciphertext)
print "%s %s"%(ciphertext, plain)
