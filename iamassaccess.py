# !/usr/bin/env python
# -*- coding: utf8 -*-

import internetarchive, json, os, sys

# Load conf file
conf_file = os.path.join('conf', 'conf.json')

if os.path.exists(conf_file) :
	with open(conf_file) as f :
		conf = json.load(f)
else :
	print 'No conf file'
	sys.exit(0)

# Walk the dir containing the files to upload
if len(sys.argv) < 2:
	print 'No folder specified'
	sys.exit(0)
	
files = []
for root, dirs, docs in os.walk(sys.argv[1]):
	for doc in docs:
		files.append(os.path.join(root, doc))

# Headers : needs to be investigated and handled
headers = dict()
headers['x-archive-auto-make-bucket'] = 1
headers['x-archive-size-hint'] = 1397759
print headers

# Metadata dictionary : all keys must be lowercase.
metadata = dict()
metadata['blagounette'] = 'kakakaka'
metadata['newmetadata'] = 'Nouvelle donnee'
metadata['year'] = "2045"

# Get the item with unique identifier. The item will be created if it does not exist.
item = internetarchive.get_item('EL065_L_1973_03_006_04_2_PF')

# Upload multiple files to an item.
item.upload(files, metadata=metadata, headers=headers, access_key=conf["access_key"], secret_key=conf["secret_key"])

# Modify metadata : modify an existing one or create new metadata
item.modify_metadata(metadata, access_key=conf["access_key"], secret_key=conf["secret_key"])