import flask

# TODO don't store these in here, but in a config file
DEBUG = True
SECRET_KEY = 'devkey'
USERNAME = 'admin'
PASSWORD = 'default'
DB_NAME = 'database.db'

app = flask.Flask(__name__)
app.config.from_object(__name__)

import index
import electricity
import events
import music
import bills
