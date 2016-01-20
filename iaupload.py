# !/usr/bin/env python
# -*- coding: utf8 -*-

import internetarchive
import sys
import os
import json

conf_file = os.path.join('conf', 'conf.json')

# Load conf file
if os.path.exists(conf_file) :
	with open(conf_file) as f :
		conf = json.load(f)
else :
	print 'No conf file'

files = []
for root, dirs, docs in os.walk(sys.argv[1]):
	for doc in docs:
		files.append(os.path.join(root, doc))

headers = dict()
headers['x-archive-auto-make-bucket'] = 1
headers['x-archive-size-hint'] = 1397759
print headers

metadata = dict()
# metadata['mediatype'] = 'image'
# metadata['creator'] = 'Bibliothèque de SciencesPo'
# metadata['Page sTitle'] = 'Législatives 1973'
metadata['Language'] = 'French'
# metadata['Year'] = '1973'
# metadata['Collections'] = ['test_collections']
metadata['Usage'] = 'Attribution-Noncommercial-No Derivative Works 3.0'
# metadata['Topics'] = ['France', 'Assemblée nationale', 'Elections législatives', 'Ve République']

# Upload a single file to an item. The item will be created if it does not exist.
item = internetarchive.get_item('Lalilou')
item.upload_file(files[0], headers=headers, metadata=metadata, access_key=conf["access_key"], secret_key=conf["secret_key"])