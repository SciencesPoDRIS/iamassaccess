# !/usr/bin/env python
# -*- coding: utf8 -*-
# Execution example : python server/iamassaccess_cli.py MODE [--metadata METADATA] [--folder FOLDER]


#
# Libs
#

import argparse
import iamassaccess
import logging
import os


#
# Functions
#

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


#
# Main
#

if __name__ == '__main__' :
	# Logging initiation routine
	log_folder = 'server/log'
	log_file = 'iamassaccess.log'
	log_level = logging.DEBUG

	# Check if the "log" folder exists, else create it
	if not os.path.isdir(log_folder) :
		os.mkdir(log_folder)
	# Init logs
	logging.basicConfig(filename = os.path.join(log_folder, log_file), filemode = 'a+', format = '%(asctime)s  |  %(levelname)s  |  %(message)s', datefmt = '%m/%d/%Y %I:%M:%S %p', level = log_level)
	logging.info('Start script')

	# Argument parser configuration + parsing of args
	parser = argparse.ArgumentParser(description='Bulk upload your items on archive.org, delete them or update their metadata!')
	parser.add_argument('mode', action='store', choices=['create', 'update', 'delete'], help="mode of operation : upload new items, update existing items' metadata or delete files")
	parser.add_argument('--metadata', dest='metadata', type=lambda x: is_valid_file(x), help="the metada csv file : headers + 1 row/file")
	parser.add_argument('--folder', dest='folder', type=lambda x: is_valid_folder(x), help="folder containing the files to be uploaded")
	args = parser.parse_args()

	# Check arguments and validity of mode + files provided
	if args.mode.lower() == 'create' and args.folder is None:
		logging.error('Mode chosen is CREATE and no files are provided to upload')
		sys.exit(0)
	elif args.mode.lower() == 'update' and args.metadata is None:
		logging.error('Mode chosen is UPDATE and no metadata file is provided to update files')
		sys.exit(0)
	elif args.mode.lower() == 'delete' and args.metadata is None:
		logging.error('Mode chosen is DELETE and no metadata file is provided to delete files')
		sys.exit(0)

	if args.mode.lower() == 'create':
		headers = dict()
		iamassaccess.createItems(args.folder, headers)
	elif args.mode.lower() == 'update':
		iamassaccess.updateItems(args.metadata)
	elif args.mode.lower() == 'delete':
		iamassaccess.deleteItems(args.metadata)

	logging.info('End script')