import flask
import logging
import mpd

from __init__ import app
import models

logger = logging.getLogger(__name__)

MPD_SINGLETON = mpd.MPDClient()


class MPDClientContextManager(object):
    def __enter__(self):
        try:
            MPD_SINGLETON.connect('localhost', 6600)
        except ConnectionAbortedError as e:
            # 10053 tells us the server disconnected us for being idle
            if '10053' not in str(e):
                raise e
            MPD_SINGLETON.disconnect()
            MPD_SINGLETON.connect('localhost', 6600)
        except mpd.ConnectionError as e:
            if 'Already connected' not in str(e):
                raise e
        return MPD_SINGLETON

    def __exit__(self, exc_type, exc_val, exc_tb):
        MPD_SINGLETON.disconnect()


def mpd_next():
    with MPDClientContextManager() as client:
        client.next()


def mpd_stop():
    with MPDClientContextManager() as client:
        client.stop()


def mpd_current_song():
    with MPDClientContextManager() as client:
        stats = client.currentsong()
        return stats['title']


def mpd_current_artist():
    with MPDClientContextManager() as client:
        stats = client.currentsong()
        return stats['artist']


def mpd_get_percent_done():
    with MPDClientContextManager() as client:
        stats = client.status()
        current_pos = float(stats['elapsed'])
        duration = float(stats['duration'])
        return current_pos/duration
