# !/usr/bin/env python
# -*- coding: utf8 -*-

import datetime
import flask
import functools
import iamassaccess

app = flask.Flask(__name__)

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

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return functools.update_wrapper(wrapped_function, f)
    return decorator

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

if __name__ == "__main__":
    app.run()