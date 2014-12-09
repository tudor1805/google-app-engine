'''
@author: Tudor Cornea
@contact: tudor.cornea@gmail.com
'''

from crons import tasks
from config import config

import webapp2

cronapp = webapp2.WSGIApplication([
    # Request handlers
    ('/crons/summary',  tasks.Summary),
    ],debug=True, config=config.config)

