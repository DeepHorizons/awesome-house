#!/usr/bin/env python3
"""
A file to start the server
"""
from __init__ import app
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    if app.config['DEBUG']:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(name)s : %(levelname)s : %(message)s')
        logger.debug('Running in debug mode')
        logger.debug(app.config)
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(name)s : %(levelname)s : %(message)s')
        logger.info('Running in production mode')
    if (app.config.get('VENMO_CLIENT_ID', None) is None) or (app.config.get('VENMO_CLIENT_SECRET', None) is None):
        logger.warning('Venmo is not set up. Set the VENMO_CLIENT_ID and VENMO_CLIENT_SECRET keys in the config file')
    app.run(host=app.config.get('HOST', None), port=app.config.get('PORT', None), threaded=True)
