"""
Index for the website
"""

# Project imports
import flask
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(name)s : %(levelname)s : %(message)s')

# Local imports
import models


DEBUG = True

app = flask.Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    return flask.render_template('index.html', title='Home')


@app.route('/events')
def events():
    return flask.render_template('events.html', title='Events')


@app.route('/electricity')
def electricity():
    return flask.render_template('electricity.html', title='Electricity')


@app.route('/music')
def music():
    return flask.render_template('music.html', title='Music')


@app.route('/bills')
def bills():
    return flask.render_template('bills.html', title='Bills')

if __name__ == '__main__':
    app.run()
