'''
@author: Tudor Cornea
@contact: tudor.cornea@gmail.com
'''

import webapp2
import logging

from google.appengine.api import memcache

class Summary(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)

    def get(self):
        logging.info("Called Summary Task")

        # This can be extended to print other stats as well ...
        stats = memcache.get_stats()
        logging.info("Hits:   %s" % stats['hits'])
        logging.info("Misses: %s" % stats['misses'])

