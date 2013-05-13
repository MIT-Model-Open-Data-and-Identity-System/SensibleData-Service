import fnmatch
import os
import sys

def get_list_of_files(rootdir, filter):
    matches = []
    for root, dirnames, filenames in os.walk(rootdir):
      for filename in fnmatch.filter(filenames, filter):
          matches.append(os.path.join(root, filename))

    return matches


#files = sorted(get_list_of_files(sys.argv[1], '*.db.orig'))

url_to_post = 'http://166.78.249.214/modis_arks/service/connectors/connector_funf/upload/?access_token=abc'
try: url_to_post = sys.argv[2]
except IndexError: pass


command = 'curl -X POST -H "Content-Type: multipart/form-data; boundary=------fdsafasdfsdf" -F "uploadedfile=@%s" '+url_to_post

limit = -1

os.system(command%(sys.argv[1]))

#for jj,filename in enumerate(files):
#    os.system(command%(filename))
#    print jj, len(files), filename
#    if jj == limit: break
