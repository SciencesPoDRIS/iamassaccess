# !/usr/bin/env python
# -*- coding: utf8 -*-

import internetarchive
import json
import logging
import os
import sys
import argparse

# Check if file argument is valid and returns it opened
def is_valid_file(arg):
    if not os.path.exists(arg):
        logging.error("The file %s does not exist" % arg)
    else:
        return open(arg, 'r')

# Check if folder argument is valid and returns its path
def is_valid_folder(arg):
    if not os.path.isdir(arg):
        logging.error("The folder %s does not exist" % arg)
    else:
        return arg

# Walk a folder and returns the list of the files it contains
def walk_files_folder(folder):
	files = []
	for dirpath, dirnames, filenames in os.walk(folder) :
		for filename in filenames :
			files.append(os.path.join(dirpath, filename))
			logging.info('File append : ' + filename)
	return files

# Load a json file (used for the metadata)
def load_metadata_file(metadata):
	if os.path.exists(os.path.join(metadata)):
		with open(metadata) as metadata_file :
			metadata = json.load(metadata_file)
	else :
		metadata = dict()
		logging.info("Specified metadata file doesn't exist : Empty metadata dictionary created")
	return metadata

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

# Load conf file
if os.path.exists(conf_file) :
	with open(conf_file) as f :
		conf = json.load(f)
	logging.info('Conf file loaded')
else :
	logging.error('No conf file provided')
	sys.exit(0)

parser = argparse.ArgumentParser(description='Bulk upload your items on archive.org or update their metadata!')
parser.add_argument('mode', action='store', choices=['create', 'update', 'delete'], help="mode of operation : upload new items, update existing items' metadata or delete files")
parser.add_argument('--metadata', dest='metadata', type=lambda x: is_valid_file(x), help="the metada file to be used to create or update the file")
parser.add_argument('--files', dest='files', type=lambda x: is_valid_folder(x), help="folder containing the files to be uploaded")
args = parser.parse_args()

# Check arguments and validity of mode + files provided
if args.mode == 'create' and args.files is None:
	logging.error('Mode chosen is CREATE and no files are provided to upload')
	sys.exit(0)
elif args.mode == 'create' and args.metadata is None:
	no_metadata = raw_input('Mode chosen is CREATE and no metadata provided.\nDo you want to upload your files without metadata?\n[Y/n]')
	print no_metadata
	if no_metadata != 'Y' and no_metadata != 'yes' and no_metadata != 'Yes':
		logging.error('User chose to exit because no metadata file provided for the specified files')
		sys.exit(0)
	else:
		logging.error('User chose to upload files without metadata')
elif args.mode == 'update' and args.metadata is None:
	logging.error('Mode chosen is UPDATE and no metadata file is provided')
	sys.exit(0)



def createItems(folder, metadata_file=None):
	files = walk_files_folder(folder)
	if metadata_file != None:
		metadata = load_metadata_file(metadata_file)

def updateItems(metadata_file):
	metadata = load_metadata_file(metadata_file)



# Headers : add additional HTTP headers to the request if needed
# RTFM : http://archive.org/help/abouts3.txt
headers = dict()



# Get the item with unique identifier. The item will be created if it does not exist.
item = internetarchive.get_item(item_id)

# Upload multiple files to an item.
item.upload(files, metadata=metadata, headers=headers, access_key=conf['access_key'], secret_key=conf['secret_key'])
logging.info('Files uploaded for item : ' + item_id)

# Modify metadata : modify an existing one or create new metadata
item.modify_metadata(metadata, access_key=conf['access_key'], secret_key=conf['secret_key'])
logging.info('Metadata modified for item : ' + item_id)

logging.info('End')



