#!/usr/bin/env python3
"""
A file to start the server
"""
from __init__ import app
import logging

if __name__ == '__main__':
    if app.config['DEBUG']:
        print(app.config)
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(name)s : %(levelname)s : %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(name)s : %(levelname)s : %(message)s')
    app.run(host='0.0.0.0', threaded=True)
