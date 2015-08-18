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

@app.route('/electricity')
def electricity():
    pass

if __name__ == '__main__':
    app.run()
