# iamassaccess
Upload and modify in mass for Internet Access : 
- upload several items in Internet Archive. Items are PDF & Images and metadata
- add metadata in existing item

## install
- mkvirtualenv iamassaccess
- pip install internetarchive
- pip install Flask
- rename the file conf/conf.default.json into conf/conf.json and edit it to put your own access key which you get, once connected to Archive.org with your login from : 
http://archive.org/account/s3.php


## usage

### write your metadata file
The metadata has to be CSV file.
Data are separated by commas.
The metadata values should be surrounded by double quotes.
The metadata keys are not case sensitive.
Te metadata values are case sensitive.
The first line has to be the list of the metadata keys.
The first column has to be the identifiers of the Internet Archive items.
For the "subject" metadata key, multiple values have to be separated by a semicolon ";".
Warning, if several lines have the same identifier, only the last line will be taken into consideration.

### execute python script
python iamassaccess_cli.py MODE [--metadata METADATA] [--folder FOLDER]
python iamassaccess_cli.py update --metadata test/metadata.csv --folder test
MODE can be create, update, delete

### launch server as daemon
python server.py &

## docs
https://blog.archive.org/2013/07/04/metadata-api/

## trivia
- can't name your items "idX" where 'X' is in an integer