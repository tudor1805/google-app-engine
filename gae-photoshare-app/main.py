'''
@author: Tudor Cornea
@contact: tudor.cornea@gmail.com
'''

from controllers import server
from config import config

import logging
import webapp2
import jinja2
import os

# Load Jinja2 Environment
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), './')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

app = webapp2.WSGIApplication([
    # Request handlers
    ('/upload',    server.Upload),
    ('/contact',   server.Contact),
    ('/slideshow', server.Slideshow),
    ('/img',       server.ImageHandler),
    ('/',          server.Gallery),
    ],debug=True, config=config.config)

# Customize the 404 handler
def handle_404(request, response, exception):
    logging.exception(exception)

    template = JINJA_ENVIRONMENT.get_template('/views/errors/404_error.html')
    response.set_status(404)
    return response.write(template.render())

app.error_handlers[404] = handle_404
