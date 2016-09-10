# !/usr/bin/env python
# -*- coding: utf8 -*-

#
# Imports
#

import datetime
import flask
from flask_cors import CORS, cross_origin
import functools
import iamassaccess
import os
from werkzeug.utils import secure_filename


#
# Config
#

UPLOAD_FOLDER = 'server/download'
ALLOWED_EXTENSIONS = set(['zip'])


#
# Funcions
#

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'thisissecrete'
CORS(app)

# Crossdomain decorator to enable cross domain request
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, datetime.timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = flask.current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and flask.request.method == 'OPTIONS':
                resp = flask.current_app.make_default_options_response()
            else:
                resp = flask.make_response(f(*args, **kwargs))
            if not attach_to_all and flask.request.method != 'OPTIONS':
                return resp

            resp.headers['Access-Control-Allow-Origin'] = origin
            resp.headers['Access-Control-Allow-Methods'] = get_methods()
            resp.headers['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                resp.headers['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return functools.update_wrapper(wrapped_function, f)
    return decorator

# Check if an extension is valid
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#
# Routing
#

@app.route("/")
@crossdomain(origin='*')
def index():
    return ''

@app.route("/create")
@crossdomain(origin='*')
def create():
    # Headers : add additional HTTP headers to the request if needed
    # RTFM : http://archive.org/help/abouts3.txt
    headers = dict()
    return iamassaccess.createItems(args.folder, headers)

@app.route("/update")
@crossdomain(origin='*')
def update():
    return iamassaccess.updateItems(args.metadata)

@app.route("/delete")
@crossdomain(origin='*')
def delete():
    return iamassaccess.deleteItems(args.metadata)

# Uploads the file and redirects the user to the URL for the uploaded file
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if flask.request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in flask.request.files:
            flask.flash('No file part')
            return flask.redirect(flask.request.url)
        file = flask.request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flask.flash('No selected file')
            return flask.redirect(flask.request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flask.flash('Ok, file uploaded')
            return flask.redirect(flask.request.url)
            # return flask.redirect(flask.url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return flask.send_from_directory(app.config['UPLOAD_FOLDER'], filename)


#
# Main
#

if __name__ == "__main__":
    app.run()