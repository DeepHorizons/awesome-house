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
import misc.music_functions as music_functions

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


@app.route('/music/control/next', methods=['PUT'])
@flask_login.login_required
def next_endpoint():
    music_functions.mpd_next()
    return flask.jsonify(status='0')


@app.route('/music/info/current_song', methods=['GET'])
@flask_login.login_required
def info_current_song():
    artist = music_functions.mpd_current_artist()
    song = music_functions.mpd_current_song()
    percent_done = music_functions.mpd_get_percent_done()
    return flask.jsonify(song=song, artist=artist, percent_done=percent_done)