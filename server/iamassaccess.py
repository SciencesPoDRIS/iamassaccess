# !/usr/bin/env python
# -*- coding: utf8 -*-

import internetarchive
import json
import csv
import logging
import os
import sys
import argparse

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

# Logs folder structure problem/error and print out correct folder structure guidelines
def print_folder_structure_problem():
	logging.error("Folder of files to upload does not comply with file structure.")
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

# Check metadata file and folder structure for correspondance (enough metadata for each file and vice-versa)
def metadata_folder_consistency(metadata_dic, files_dic):
	for file in files_dic:
	 	if file not in metadata_dic.keys():
	 		logging.error("Missing metadatas for file %s" % file)
	 		sys.exit(0)
	for metadata in metadata_dic:
		if metadata not in files_dic.keys():
			logging.error("Metadata in the file metadata.csv isn't attributed to a file")
			sys.exit(0)

# Walk a folder and returns the list of the names of the files it contains
def walk_files_folder(folder):
	filenames = []
	for root, dirs, files in os.walk(folder):
		for filename in files :
			filenames.append(os.path.join(root, filename))
			logging.info('File append : ' + filename)
	return filenames

# Verify the structure of a folder of files to upload (and presence of metadata file)
# Return the dictionary of metadata and the dictionary of files
def walk_files_upload(folder):
	items = os.listdir(folder)

	if 'metadata.csv' in items:
		metadata_dic = load_csv_metadata_file(os.path.join(folder, 'metadata.csv'))
	else:
		logging.error('No metadata file provided. A file named \'metadata.csv\' should be in the zip folder.')
		sys.exit(0)

	files_dic = {}
	for item in items:
		if item[0] != '.' and item != "metadata.csv":
			if not os.path.isdir(os.path.join(folder, item)):
				print_folder_structure_problem()
			else:
				files = os.listdir(os.path.join(folder, item))
				fullpathfiles = []
				for file in files:
					if not os.path.isfile(os.path.join(folder, item, file)):
						print_folder_structure_problem()
					elif file[0] != '.':
						fullpathfile = os.path.join(folder, item, file)
						fullpathfiles.append(fullpathfile)
				files_dic[item] = fullpathfiles

	metadata_folder_consistency(metadata_dic, files_dic)
	return metadata_dic, files_dic

# Load a csv file (used for the metadata)
def load_csv_metadata_file(metadata):
	if os.path.exists(os.path.join(metadata)):
		metadata_dict = dict()
		with open(metadata) as metadata_file :
			metadata_csv = csv.reader(metadata_file)
			headers = metadata_csv.next()[1:] # list of attributes names minus file identifiers in the first columns
			for line in metadata_csv:
				filename = line[0]
				metadata_dict[filename] = dict()
				attributes = line[1:]
				for i in range(len(attributes)):
					key = headers[i].lower()
					value = attributes[i]
					metadata_dict[filename][key] = value
		metadata = metadata_dict
	else :
		metadata = None
		logging.info('Specified metadata file doesn\'t exist or impossible to load')
	return metadata

# Load a json file to a dictionary (used for the metadata)
def load_json_metadata_file(metadata):
	if os.path.exists(os.path.join(metadata)):
		with open(metadata) as metadata_file :
			metadata = json.load(metadata_file)
	else :
		metadata = None
		logging.info('Specified metadata file doesn\'t exist or impossible to load')
	return metadata

# Uploads files in folders in new items or in existing items if they exists
def createItems(folder, headers):
	try:
		log_folder
	except NameError:
		init()
	if is_valid_folder(folder):
		metadata, files = walk_files_upload(folder)
		for folder in files:
			item = internetarchive.get_item(folder)
			# Check if item already exists
			if item.exists:
				logging.error('Item "' + folder + '" already exists. Please use the "UPDATE" mode to update its metadata.')
			# If item does not already exist, upload it
			else :
				files_for_item = files[folder]
				metadata_for_item = metadata[folder]
				item.upload(files_for_item, metadata=metadata_for_item, headers=headers, access_key=conf['access_key'], secret_key=conf['secret_key'])
				logging.info('Files uploaded for item : ' + folder)
	else:
		logging.error('The folder ' + folder + ' does not exist.')

# Modify metadata : modify an item's metadata or create new one
def updateItems(metadata_file):
	try:
		log_folder
	except NameError:
		init()
	if is_valid_file(metadata_file):
		metadata = load_csv_metadata_file(metadata_file)
		for file in metadata:
			item = internetarchive.get_item(file)
			# Check if item already exists
			if not item.exists:
				logging.error('Item "' + file + '" does not exist. Please use the "CREATE" mode to create it.')
			# If item does not already exist, upload it
			else:
				item.modify_metadata(metadata[file], access_key=conf['access_key'], secret_key=conf['secret_key'])
				logging.info('Metadata modified for item : ' + str(item.identifier))
	else:
		logging.error('The file ' + metadata_file + ' does not exist.')

# Delete a list of items (All the files are not deleted)
def deleteItems(metadata_file):
	try:
		log_folder
	except NameError:
		init()
	if is_valid_file(metadata_file) :
		metadata = load_csv_metadata_file(metadata_file)
		for item_name in metadata:
			item = internetarchive.get_item(item_name)
			# Check if item already exists
			if item.exists :
				# Gets files in the item
				files = item.get_files(glob_pattern='*')
				# Deletes them one by one
				for file in files:
					file.delete(access_key=conf['access_key'], secret_key=conf['secret_key'])
				logging.info('All files of the item "' + item_name + '" are deleted.')
			else :
				logging.error('Item "' + item_name + '" does not exist. Can\'t delete an item that doesn\'t exist.')
	else :
		logging.error('The file ' + metadata_file + ' does not exist.')

# Init log and argparse
def init():
	global conf

	# Logging initiation routine
	log_folder = 'server/log'
	log_file = 'iamassaccess.log'
	log_level = logging.DEBUG

	# Check if the "log" folder exists, else create it
	if not os.path.isdir(log_folder) :
		os.mkdir(log_folder)
	# Init logs
	logging.basicConfig(filename = os.path.join(log_folder, log_file), filemode = 'a+', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = log_level)
	logging.info('Start')

	# Load conf file
	conf_file = os.path.join('server', 'conf', 'conf.json')
	if os.path.exists(conf_file) :
		with open(conf_file) as f :
			conf = json.load(f)
		logging.info('Conf file loaded')
	else :
		logging.error('No conf file provided or wrong path : ' + conf_file)
		sys.exit(0)

	# Headers : add additional HTTP headers to the request if needed
	# RTFM : http://archive.org/help/abouts3.txt
	headers = dict()