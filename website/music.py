"""
Index for the website
"""

# Project imports
import flask
import logging

# Local imports
from __init__ import app
import models


@app.route('/music')
def music():
    return flask.render_template('music.html', title='Music')
