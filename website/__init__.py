import flask
import flask_wtf.csrf
import logging

logger = logging.getLogger(__name__)

# TODO don't store these in here, but in a config file
DEBUG = True
TESTING = DEBUG
SECRET_KEY = 'devkey'
DB_NAME = 'database.db'

app = flask.Flask(__name__)
app.config.from_object(__name__)
try:
    app.config.from_envvar('AWESOME_HOUSE_WEBSITE_CONFIG_SETTINGS')
except RuntimeError:
    logger.critical('No external configuration found, using default values. Set `AWESOME_HOUSE_WEBSITE_CONFIG_SETTINGS` to point to a configuration file')
flask_wtf.csrf.CsrfProtect(app)

import views
