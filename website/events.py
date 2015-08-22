"""
Index for the website
"""

# Project imports
import flask
import logging

# Local imports
from __init__ import app
import models


@app.route('/events')
def events():
    return flask.render_template('events.html', title='Events')
