'''
@author: Tudor Cornea
@contact: tudor.cornea@gmail.com
'''

from google.appengine.ext import ndb

def album_key(album_name):
    """Constructs a Datastore key for a Photo Album entity and an album_name"""
    return ndb.Key('PhotoAlbum', album_name)

class PhotoUpload(ndb.Model):
    """Models an individual Photo Upload entry"""
    upload_user = ndb.UserProperty(indexed=True)
    image = ndb.BlobProperty(indexed=False)
    description = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

