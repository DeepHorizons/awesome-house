"""
Index for the website
"""

# Project imports
import flask
import logging

# Local imports
from __init__ import app
import models


@app.route('/bills')
def bills():
    return flask.render_template('bills.html', title='Bills')
