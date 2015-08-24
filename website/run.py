#!/usr/bin/env python3
"""
A file to start the server
"""

from __init__ import app

if __name__ == '__main__':
    print(app.config)
    app.run(host='0.0.0.0', threaded=True)
