'''
@author: Tudor Cornea
@contact: tudor.cornea@gmail.com
'''

import webapp2

import os

import endpoints
from protorpc import *

from api.location_api_messages import LocationRequestMessage
from api.location_api_messages import LocationResponseMessage

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db

from models.user_position import *

import geo.geomodel
import geo.geotypes
from geo.geomodel import GeoModel

from api.location_api_messages import LocationRequestMessage                                                                                                       
from api.location_api_messages import LocationResponseMessage

# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'                                                                                                     
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID


package = 'MeetUpLocation'

@endpoints.api(name='meetup_location', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID,
                                   ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE])
class LocationApi(remote.Service):
    """ MeetUp Location API v1."""

    def _retrieve_location(self, user, device_id):
        # Check if the parameters are valid
        if not user or not device_id:
            raise ValueError

        # Get the existing location
        existing_locations = UserPosition.all() \
                                .filter('user =', user) \
                                .filter('device =', device_id)
        return existing_locations[0]

    def _update_location(self, user, device_id, location):
        # Check if the parameters are valid
        if not user or not device_id or not location:
            raise ValueError

        # Delete any existing location settings
        existing_locations = UserPosition.all() \
                                .filter('user =', user) \
                                .filter('device =', device_id)
        for user_position in existing_locations:
           user_position.delete()

        # Store the new location
        user_pos = UserPosition(location = location,
                                user = user,
                                device = device_id)
        user_pos.update_location()
        user_pos.put()

    @endpoints.method(LocationRequestMessage, message_types.VoidMessage,
                      path='meetup_location', http_method='POST',
                      name='update_location')
    def update_location(self, request):
        try:
            user = users.get_current_user()
            # if not user:
            #     auth_url = users.create_login_url(self.request.uri)
            #     return self.redirect(auth_url)

            location_pt = db.GeoPt(request.latitude, request.longitude)
            # self._update_location(user, request.device_id, location_pt)
            print "User is [%s]" % str(user)
        except ValueError:
            return self.error(400)

        return message_types.VoidMessage()

    @endpoints.method(message_types.VoidMessage, LocationResponseMessage,
                      path='meetup_location', http_method='GET',
                      name='retrieve_location')
    def retrieve_location(self, unused_request):
        return LocationResponseMessage(msg = "Not Implemented !")

