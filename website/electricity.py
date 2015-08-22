"""
Index for the website
"""

# Project imports
import flask
import logging

# Local imports
from __init__ import app
import models


@app.route('/electricity')
def electricity():
    return flask.render_template('electricity.html', title='Electricity')
