# !/usr/bin/env python
# -*- coding: utf8 -*-

import internetarchive, json, logging, os, sys

# Load conf file
conf_file = os.path.join('conf', 'conf.json')
log_folder = 'log'
log_level = logging.DEBUG
item_id = 'new_al_item'

# Check that log folder exists, else create it
if not os.path.exists(log_folder) :
	os.makedirs(log_folder)
# Create log file path
log_file = os.path.join(log_folder, sys.argv[0].replace('.py', '.log'))
# Init logs
logging.basicConfig(filename = log_file, filemode = 'a+', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = log_level)
logging.info('Start')

if os.path.exists(conf_file) :
	with open(conf_file) as f :
		conf = json.load(f)
else :
	logging.error('No conf file')
	sys.exit(0)

# Walk the dir containing the files to upload
if len(sys.argv) < 2 :
	logging.error('No folder specified')
	sys.exit(0)

files = []
for dirpath, dirnames, filenames in os.walk(sys.argv[1]) :
	for filename in filenames :
		files.append(os.path.join(dirpath, filename))
		logging.info('File append : ' + filename)

# Headers : add additional HTTP headers to the request if needed
# RTFM : http://archive.org/help/abouts3.txt
headers = dict()

# Load metadata as json file
# ToDo : all the keys have to be in lowercase
if os.path.exists(os.path.join(sys.argv[1], 'metadata.json')) :
	with open(os.path.join(sys.argv[1], 'metadata.json')) as metadata_file :
		metadata = json.load(metadata_file)
# If no metadata file for this item
else :
	metadata = dict()
	logging.info('No metadata file for item : ' + item_id)

# Get the item with unique identifier. The item will be created if it does not exist.
item = internetarchive.get_item(item_id)

# Upload multiple files to an item.
item.upload(files, metadata=metadata, headers=headers, access_key=conf['access_key'], secret_key=conf['secret_key'])
logging.info('Files uploaded for item : ' + item_id)

# Modify metadata : modify an existing one or create new metadata
item.modify_metadata(metadata, access_key=conf['access_key'], secret_key=conf['secret_key'])
logging.info('Metadata modified for item : ' + item_id)

logging.info('End')