def transform(document):
	document
	keyset=document.keys()
	print keyset
	for key in keyset[:]:
		print key
		data=document[key]
		try:
			other_keys=data.keys()
			if len(other_keys)>0:
				transform(data)
	
		except AttributeError:
			print ''

		if '.' in key:
			new_key=key.replace('.','_')
			document[new_key]=document[key]
			document.pop(key,'None')
		if '$' in key:
			new_key=key.replace('$','_')
			document[new_key]=document[key]
			document.pop(key,'None')
		

	return document
