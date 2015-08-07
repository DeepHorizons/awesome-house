"""
Index for the website
"""

# Project imports
import flask

# Local imports


DEBUG = True

app = flask.Flask(__name__)
app.config.from_object(__name__)




@app.route('/')
def index():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run()
