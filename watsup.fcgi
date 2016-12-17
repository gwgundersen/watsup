#!/home1/gregoso6/public_html/watsup/venv/bin/python

from flup.server.fcgi import WSGIServer
from watsup import app as application

WSGIServer(application).run()
