"""
Index for the website
"""

# Project imports
import flask
import logging
import flask_login

# Local imports
from __init__ import app
import models

logger = logging.getLogger(__name__)


@app.route('/bills')
@flask_login.login_required
def bills():
    return flask.render_template('bills.html', title='Bills')
