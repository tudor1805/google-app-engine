'''
@author: Tudor Cornea
@contact: tudor.cornea@gmail.com
'''

from google.appengine.ext import ndb

def generate_key(user_id):
    """ Constructs a Datastore key for a User Settings entity """
    return ndb.Key('UUID', user_id)

class UserSettings(ndb.Model):
    """ Models an individual User Settings entry """
    user = ndb.StringProperty(indexed=True)
    device = ndb.StringProperty(indexed=True)
    search_radius = ndb.IntegerProperty(indexed=False)
    visible = ndb.BooleanProperty(indexed=False)

