# !/usr/bin/env python
# -*- coding: utf8 -*-

import internetarchive
import sys
import os

access_key = '8wTtUBty6wNXtoQ8'
secret_key = 'lYpcqCksqK2AdCpe'

files = []
for root, dirs, docs in os.walk(sys.argv[1]):
	for doc in docs:
		files.append(root + doc)

headers = dict()
headers['x-archive-auto-make-bucket'] = 1
headers['x-archive-size-hint'] = 1397759


print headers

# metadata = dict()
# metadata['mediatype'] = 'pdf'
# metadata['creator'] = 'Bibliothèque de SciencesPo'
# metadata['Page sTitle'] = 'Législatives 1973'
# metadata['Language'] = 'French'
# metadata['Year'] = '1973'
# metadata['Collections'] = ['archiveselectoralesducevipof', 'additional_collections']
# metadata['Usage'] = 'Attribution-Noncommercial-No Derivative Works 3.0'
# metadata['Topics'] = ['France', 'Assemblée nationale', 'Elections législatives', 'Ve République']

item = internetarchive.Item('Pictures')

print item.exists

item.upload_file(files[0], headers=headers)