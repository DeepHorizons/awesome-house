import flask
import logging
from urllib.parse import urlparse, urljoin
from flask import request, url_for

logger = logging.getLogger(__name__)
