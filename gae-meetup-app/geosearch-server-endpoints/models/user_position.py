'''
@author: Tudor Cornea
@contact: tudor.cornea@gmail.com
'''

from google.appengine.ext import db
from geo.geomodel import GeoModel

class UserPosition(GeoModel):
    """ Models an individual User Position entry """
    user   = db.StringProperty(indexed=True)
    device = db.StringProperty(indexed=True)
    date   = db.DateTimeProperty(auto_now_add=True)

    def _get_latitude(self):
        return self.location.lat if self.location else None

    def _set_latitude(self, lat):
        if not self.location:
            self.location = db.GeoPt()
        self.location.lat = lat

    latitude = property(_get_latitude, _set_latitude)

    def _get_longitude(self):
        return self.location.lon if self.location else None

    def _set_longitude(self, lon):
        if not self.location:
            self.location = db.GeoPt()

        self.location.lon = lon

    def __str__(self):
        return self.user + " " + self.device + " " + str(self.date) + " " + str(self._get_latitude()) + " " + str(self._get_longitude())

    def __repr__(self):
        return self.__str__()

    longitude = property(_get_longitude, _set_longitude)
