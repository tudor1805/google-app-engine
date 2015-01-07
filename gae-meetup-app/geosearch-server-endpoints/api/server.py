'''
@author: Tudor Cornea
@contact: tudor.cornea@gmail.com
'''

import os
from pprint import pprint
import logging

import endpoints
from protorpc import *

import geo.geomodel
import geo.geotypes
from geo.geomodel import GeoModel

from api.messages import *

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db

from models.user_settings import *
from models.user_position import *

# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = '582179463281-t6h3hf1nkf5n5nadsb7gd87htmhfrhjk.apps.googleusercontent.com'
WEB_CLIENT_ID = '582179463281-t6h3hf1nkf5n5nadsb7gd87htmhfrhjk.apps.googleusercontent.com'
ANDROID_AUDIENCE = WEB_CLIENT_ID

package = 'MeetUp'

""" MeetUp Server API v1."""
@endpoints.api(name='server_api', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID,
                                   ANDROID_CLIENT_ID,
                                   endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE])
class ServerApi(remote.Service):
    """ ==== MeetUp Service API ==== """

    """ ==== Settings API ==== """
    def _retrieve_settings(self, user_id, device_id):
        # Check if the parameters are valid
        if not user_id or not device_id:
            raise ValueError

        uuid = generate_key(user_id)
        settings = UserSettings.query(ancestor = uuid).fetch()
        return settings[0]

    def _update_settings(self, user_id, device_id, search_radius, visible):
        # Check if the parameters are valid
        if not user_id or not device_id or not search_radius:
            raise ValueError

        uuid = generate_key(user_id)

        # Delete any existing settings
        ndb.delete_multi(
            UserSettings.query(ancestor = uuid).fetch(keys_only=True)
        )

        # Create the new settings
        setting = UserSettings(parent = uuid)
        setting.user = user_id
        setting.device = device_id
        setting.search_radius = search_radius
        setting.visible = visible
        setting.put()

    @endpoints.method(SettingsRequestMessage, message_types.VoidMessage,
                      path='settings', http_method='POST',
                      name='update_settings')
    def update_settings(self, request):
        try:
            self._update_settings(request.user_id,
                                  request.device_id,
                                  request.search_radius,
                                  request.is_visible)
        except ValueError:
            return self.error(400)

        return message_types.VoidMessage()

    """ ==== Location API ==== """
    def _retrieve_location(self, user_id, device_id):
        # Check if the parameters are valid
        if not user_id or not device_id:
            raise ValueError

        # Get the existing location
        existing_locations = UserPosition.all() \
                                .filter('user =', user_id)
        return existing_locations[0]

    def _update_location(self, user_id, device_id, location):
        # Check if the parameters are valid
        if not user_id or not device_id or not location:
            raise ValueError

        # Delete any existing location settings
        existing_locations = UserPosition.all() \
                                .filter('user =', user_id)
        for user_position in existing_locations:
           user_position.delete()

        # Store the new location
        user_pos = UserPosition(location = location,
                                user = user_id,
                                device = device_id)
        user_pos.update_location()
        user_pos.put()

    @endpoints.method(LocationRequestMessage, message_types.VoidMessage,
                      path='location', http_method='POST',
                      name='update_location')
    def update_location(self, request):
        try:
            location_pt = db.GeoPt(request.latitude, request.longitude)
            self._update_location(request.user_id,
                                  request.device_id,
                                  location_pt)
        except ValueError:
            return self.error(400)

        return message_types.VoidMessage()

    """ ==== Query API ==== """
    def _proximity_query(self, user_id, device_id, user_friends_ids):
        # Check if the parameters are valid
        if not user_id or not device_id or not user_friends_ids:
            raise ValueError

        settings = self._retrieve_settings(user_id, device_id)
        location = self._retrieve_location(user_id, device_id)

        """ Get a list with ids of the visible friends """
        search_users_ids = []
        for friend_id in user_friends_ids:
            try:
                uuid = generate_key(friend_id)
                friend_settings = UserSettings.query(ancestor = uuid).fetch()[0]
                if friend_settings and friend_settings.visible:
                    # Get the existing location
                    existing_location = UserPosition.all() \
                                        .filter('user =', friend_id)[0]
                    if existing_location:
                        search_users_ids.append(friend_id)
            except IndexError:
                logging.info("User %s not found" % friend_id)

        if search_users_ids:
            query_users = UserPosition.all().filter('user IN', search_users_ids)

            # Find all existing users within search_radius meters
            query_result = UserPosition.proximity_fetch(
                            query_users,
                            location.location,
                            max_results = 100,
                            max_distance = settings.search_radius)
        else:
            query_result = []

        return query_result

    def _format_friend_location(self, friend_id, latitude, longitude):
        friend = FriendLocation()
        friend.user_friend_id = friend_id
        friend.latitude       = latitude
        friend.longitude      = longitude
        return friend

    """ Construct dummy data, to be used for testing """
    def _dummy_user_data(self, user_data):
        self._update_settings(user_data['user_id'],
                               user_data['device_id'],
                               user_data['search_radius'],
                               user_data['is_visible'])

        location_pt = db.GeoPt(user_data['location']['latitude'], user_data['location']['longitude'])
        self._update_location(user_data['user_id'], user_data['device_id'], location_pt)

    def _dummy_data(self):
         users_data = [
           {
            'user_id'       : 'test_user1',
            'device_id'     : 'test_device1',
            'search_radius' : 1000,
            'is_visible'    : True,
            'location' : {
               'latitude'   : 43.81136,
               'longitude'  : 28.57196
             }
           },
           {
            'user_id'       : 'test_user2',
            'device_id'     : 'test_device2',
            'search_radius' : 1000,
            'is_visible'    : True,
            'location' : {
               'latitude'   : 43.80987,
               'longitude'  : 28.58613
             }
           },
           {
            'user_id'       : 'test_user3',
            'device_id'     : 'test_device3',
            'search_radius' : 1000,
            'is_visible'    : True,
            'location' : {
               'latitude'   : 43.81175,
               'longitude'  : 28.57613
             }
           },
           {
            'user_id'       : 'test_user4',
            'device_id'     : 'test_device4',
            'search_radius' : 1000,
            'is_visible'    : True,
            'location' : {
               'latitude'   : 43.81608,
               'longitude'  : 28.57975
             }
           },
           {
            'user_id'       : 'test_user5',
            'device_id'     : 'test_device5',
            'search_radius' : 1000,
            'is_visible'    : True,
            'location' : {
               'latitude'   : 43.81498,
               'longitude'  : 28.58795
             }
           },
         ]
 
         for user_data in users_data:
             self._dummy_user_data(user_data)

    """ Return dummy answer, to be used for testing """
    def _dummy_answer(self):
        answer = QueryResponseMessage()
        near_friends = []
        near_friends.append(self._format_friend_location("Vasile", 43.81136, 28.57196))
        near_friends.append(self._format_friend_location("Andrei", 43.80987, 28.58613))
        near_friends.append(self._format_friend_location("Mircea", 43.81175, 28.57613))
        near_friends.append(self._format_friend_location("Ana", 43.81608, 28.57975))
        near_friends.append(self._format_friend_location("Daniel", 43.81498, 28.58795))
        near_friends.append(self._format_friend_location("Ionut", 43.82494, 28.58198))
        near_friends.append(self._format_friend_location("Alexandra", 43.82033, 28.58535))
        near_friends.append(self._format_friend_location("Mihai", 43.80791, 28.56555))
        near_friends.append(self._format_friend_location("Gigel", 43.80066, 28.57840))
        answer.near_friends = near_friends
        return answer

    @endpoints.method(QueryRequestMessage, QueryResponseMessage,
                      path='query', http_method='POST',
                      name='query_near_friends')
    def post_query(self, request):
        answer = QueryResponseMessage()
        try:
            near_friends_loc = self._proximity_query(request.user_id,
                                                     request.device_id,
                                                     request.user_friend_ids)
            near_friends_list = []
            for friend_loc in near_friends_loc:
                formatted_friend = self._format_friend_location(
                                         friend_loc.user,
                                         friend_loc._get_latitude(),
                                         friend_loc._get_longitude())
                near_friends_list.append(formatted_friend)
            answer.near_friends = near_friends_list
        except IndexError:
            answer.near_friends = []
        return answer

""" Exposed API """
APPLICATION = endpoints.api_server( [ ServerApi ])

