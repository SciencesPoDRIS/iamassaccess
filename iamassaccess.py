# !/usr/bin/env python
# -*- coding: utf8 -*-

import internetarchive
import json
import csv
import logging
import os
import sys
import argparse
from collections import defaultdict

# Check if file argument is valid and returns it opened
def is_valid_file(arg):
    if not os.path.exists(arg):
        logging.error("The file %s does not exist" % arg)
    else:
        return arg

# Check if folder argument is valid and returns its path
def is_valid_folder(arg):
    if not os.path.isdir(arg):
        logging.error("The folder %s does not exist" % arg)
    else:
        return arg

# # Walk a folder and returns the list of the names of the files it contains
# def walk_files_folder(folder):
# 	filenames = []
# 	for root, dirs, files in os.walk(folder):
# 		for filename in files :
# 			filenames.append(os.path.join(root, filename))
# 			logging.info('File append : ' + filename)
# 	return filenames

# Load a csv file (used for the metadata)
def load_csv_metadata_file(metadata):
	if os.path.exists(os.path.join(metadata)):
		metadata_dict = defaultdict(lambda : defaultdict())
		with open(metadata) as metadata_file :
			metadata_csv = csv.reader(metadata_file)
			headers = metadata_csv.next()
			for line in metadata_csv:
				filename = line[0]
				for attribute in range(1, len(line)):
					key = "attribute" + str(attribute)
					value = line[attribute]
					metadata_dict[filename][key] = value.lower()
		metadata = metadata_dict
	else :
		metadata = None
		logging.info("Specified metadata file doesn't exist or impossible to load")
	return metadata

# # Load a json file to a dictionary (used for the metadata)
# def load_json_metadata_file(metadata):
# 	if os.path.exists(os.path.join(metadata)):
# 		with open(metadata) as metadata_file :
# 			metadata = json.load(metadata_file)
# 	else :
# 		metadata = None
# 		logging.info("Specified metadata file doesn't exist or impossible to load")
# 	return metadata

def createItems(folder, metadata_file=None):
	files = walk_files_folder(folder)
	if metadata_file != None:
		metadata = load_metadata_file(metadata_file)

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


def walk_files_upload(folder):
	items = os.listdir(folder)
	
	if "metadata.csv" in items:
		metadata = load_csv_metadata_file('metadata.csv')
	else:
		no_metadata = raw_input('Mode chosen is CREATE and no metadata provided.\nDo you want to upload your files without metadata?\n[Y/n]')
		if no_metadata != 'Y' and no_metadata != 'yes' and no_metadata != 'Yes':
			logging.error('User chose to exit because no metadata file provided for the specified files')
			sys.exit(0)
		else:
			logging.error('User chose to upload files without metadata')
	
	files_dic = {}
	for item in items:
		if item != ".DS_Store" and item != "metadata.csv":
			if not os.path.isdir(os.path.join(folder, item)):
				logging.error("Folder of files to upload does not comply with file structure")
				print """
Folder of files to upload does not comply with following file structure
- folder
  - file_1
    - doc_to_upload
    - doc_to_upload
    - doc_to_upload
  - file_2
    - doc_to_upload
    - doc_to_upload
    - doc_to_upload
  - metadata.csv
"""
				sys.exit(0)
			files = os.listdir(os.path.join(folder, item))
	print files
	return metadata, files

walk_files_upload(args.files)

# def updateItems(metadata_file):
# 	metadata = load_metadata_file(metadata_file)


# # Headers : add additional HTTP headers to the request if needed
# # RTFM : http://archive.org/help/abouts3.txt
# headers = dict()



# # Get the item with unique identifier. The item will be created if it does not exist.
# item = internetarchive.get_item(item_id)

# # Upload multiple files to an item.
# item.upload(files, metadata=metadata, headers=headers, access_key=conf['access_key'], secret_key=conf['secret_key'])
# logging.info('Files uploaded for item : ' + item_id)

# # Modify metadata : modify an existing one or create new metadata
# item.modify_metadata(metadata, access_key=conf['access_key'], secret_key=conf['secret_key'])
# logging.info('Metadata modified for item : ' + item_id)

logging.info('End')



