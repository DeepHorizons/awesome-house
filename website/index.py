"""
Index for the website
"""

# Project imports
import flask
import logging

# Local imports
from __init__ import app
import models


@app.route('/')
def index():
    return flask.render_template('index.html', title='Home')
