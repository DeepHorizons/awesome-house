import flask
import flask_wtf.csrf

# TODO don't store these in here, but in a config file
DEBUG = True
TESTING = True
SECRET_KEY = 'devkey'
USERNAME = 'admin'
PASSWORD = 'default'
DB_NAME = 'database.db'

app = flask.Flask(__name__)
app.config.from_object(__name__)
flask_wtf.csrf.CsrfProtect(app)

import views.index
import views.electricity
import views.events
import views.music
import views.bills
import views.login
