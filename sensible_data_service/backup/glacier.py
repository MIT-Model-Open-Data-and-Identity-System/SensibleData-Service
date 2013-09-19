import boto
import shelve
import sys
import time
import json


def download(inventory, vault, fname):
	if fname not in inventory:
		print fname, ' not in inventory!'
		return
	archive_id = inventory[fname] 
	retrieve_job = vault.retrieve_archive(archive_id, sns_topic=GLACIER['SNS_TOPIC'])
	jobid = retrieve_job.id
	print 'job id = ', jobid
	while retrieve_job.completed is False:
		print 'file not ready, sleeping for 10 min...'
		time.sleep(600)	    
		retrieve_job = vault.get_job(jobid)
	retrieve_job.download_to_file(fname)
	print 'found, saved as ', fname    


def upload(inventory, vault, fname):
	fin = open(fname, 'rb')
	archive_id = vault.create_archive_from_file(filename=fname, file_obj=fin)
	inventory[fname] = archive_id
	fin.close()
	return archive_id

def local_inventory(inventory):
	print '---------------------------'
	print 'local inventory            '
	print
	print 'filename -> archive_id'
	print '---------------------------'
	for k, v in inventory.items():
		print '%s -> %s' % (k, v) 


def list_jobs(vault):
	for j in vault.list_jobs():
		print j.__dict__


if __name__ == "__main__":
	inventory = shelve.open('inventory')
	glacier_connection = boto.connect_glacier(aws_access_key_id=GLACIER['ACCESS_KEY_ID'],
                                    aws_secret_access_key=GLACIER['SECRET_ACCESS_KEY'],
                                    region_name='eu-west-1')
	vault = glacier_connection.get_vault(GLACIER['VAULT'])

	if len(sys.argv) < 2:
   		print 'usage: ul | dl | inv | jobs'
   	elif sys.argv[1] == 'jobs':
   		list_jobs(vault)
   	elif sys.argv[1] == 'ul':
   		upload(inventory, vault, sys.argv[2])
   	elif sys.argv[1] == 'dl':
   		download(inventory, vault, sys.argv[2])
   	elif sys.argv[1] == 'inv':
   		local_inventory(inventory)
   	else:
   		print 'usage: ul | dl | inv'
	inventory.close()
