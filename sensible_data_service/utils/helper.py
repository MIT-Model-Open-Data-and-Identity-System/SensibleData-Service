import time
from Crypto.Hash import HMAC
from Crypto.Hash import SHA512

def get_timestamp():
    return int(round(time.time() * 1000))
#    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') # Format : "2013-06-08 12:01:15" TODO: make it fine-grained. ms?


# TODO: Ask which parts of the data must go inside the log audit and which not to save space and time
# Right now is a 1:1 copy
def extract_info(data):
    return data


def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def extract(myDict, myList):
    if myDict is None:
        return
    for value in myDict.values():
        if isinstance(value, dict):
            extract(value, myList)
        else:
            myList.append(value)


def checksum(saved_data):
    outputList = []
    extract(saved_data, outputList)
    resultList = convert(outputList)
    resultList.sort() # sort the values, done so when later it will be checked, the hashes will be the same
    return ''.join(resultList) # from list to string

# TODO: add method form computing the "study_username" and another one to retrive it. So this will be the only place to change the format of the collections insted of hard-coding everywhere.

def link(checksum, previous_link, study_user_key):
    hmac = HMAC.new(study_user_key)
    hmac.update(checksum)
    hmac.update(previous_link)
    return hmac.hexdigest()

# key = 128 hex digits
def do_hash(rounds, key):
    for i in range(0,rounds):
        h = SHA512.new()
        h.update(key)
        key = h.hexdigest()
    return str(key)


# PBKDF2 with random, unique salts and constant-time comparison:





