"""
Index for the website
"""

# Project imports
import flask
import logging

# Local imports
from __init__ import app
import models

logger = logging.getLogger(__name__)


@app.route('/bills')
def bills():
    return flask.render_template('bills.html', title='Bills')
