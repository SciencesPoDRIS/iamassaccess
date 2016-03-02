# !/usr/bin/env python
# -*- coding: utf8 -*-

import internetarchive
import json
import logging
import os
import sys
import argparse

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

# Parser test of existence of file of myenglishisbad
def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist" % arg)
    else:
        return open(arg, 'r')

parser = argparse.ArgumentParser(description='Bulk upload your items on archive.org or update their metadata!')
parser.add_argument('mode', action='store', choices=['create', 'update'], help="mode of operation : upload new items or update existing items' metadata")
parser.add_argument('--metadata', dest='metadata', type=lambda x: is_valid_file(parser, x), help="the metada file to be used to create or update the file")
parser.add_argument('--files', dest='files', help="folder containing the files to be uploaded")
args = parser.parse_args()

print args

if args.mode == 'create' and args.files is None:
	logging.error('Mode chosen is CREATE and no files are provided to upload')
	sys.exit(0)
elif args.mode == 'create' and args.metadata is None:
	no_metadata = raw_input('Mode chosen is CREATE and no metadata provided. Do you want to upload your files without metadata? [Y/n]')
	if no_metadata != 'Y' or no_metadata != 'yes' or no_metadata != 'Yes':
		logging.error('No metadata file provided for the specified files.')
		sys.exit(0)
	else:
		logging.error('No metadata file provided. Uploading files without metadata')
elif args.mode == 'update' and args.metadata is None:
	logging.error('Mode chosen is UPDATE and no metadata file is provided')
	sys.exit(0)

if os.path.exists(conf_file) :
	with open(conf_file) as f :
		conf = json.load(f)
else :
	logging.error('No conf file provided')
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