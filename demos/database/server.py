import os
import sys
from pathlib import Path

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = str(Path(__file__).parents[2])
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

from demos.database.app import create_app

"""
Flask自带的WSGI server每来一个请求新建一个线程, 因此不要在生产中使用
 requests are each handled in a new thread. How many threads your server can handle concurrently depends entirely 
 on your OS and what limits it sets on the number of threads per process. The implementation uses the SocketServer.
 ThreadingMixIn class, which sets no limits to the number of threads it can spin up.
the Flask server is designed for development only. It is not a production-ready server. Don't rely on it to run
 your site on the wider web. Use a proper WSGI server (like gunicorn or uWSGI) instead.
"""

"""gunicorn --workers=3 server:app -b 0.0.0.0:9996"""
app = create_app()
