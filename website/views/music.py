"""
Index for the website
"""

# Project imports
import flask
import logging
import flask_login
import requests

# Local imports
from __init__ import app
import models

logger = logging.getLogger(__name__)


@app.route('/music')
@flask_login.login_required
def music():
    return flask.render_template('music.html', title='Music')


@app.route('/music/get_music')
@flask_login.login_required
def get_music():
    r = requests.get('http://127.0.0.1:8000/', stream=True)
    return flask.Response(flask.stream_with_context(r.iter_content()), content_type=r.headers['content-type'])
