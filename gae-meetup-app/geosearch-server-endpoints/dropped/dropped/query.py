'''
@author: Tudor Cornea
@contact: tudor.cornea@gmail.com
'''

import webapp2

import endpoints
from protorpc import *

from api.query_api_messages import FriendLocation
from api.query_api_messages import QueryRequestMessage
from api.query_api_messages import QueryResponseMessage

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db

from models.user_position import *
from models.user_settings import *

import geo.geomodel
import geo.geotypes
from geo.geomodel import GeoModel

import json

from pprint import pprint

# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'                                                                                                     
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

package = 'MeetUpQuery'

@endpoints.api(name='meetup_query', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID,
                                   ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE])
class QueryApi(remote.Service):
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

    def _retrieve_settings(self, user, device_id):
        # Check if the parameters are valid
        if not user or not device_id:
            raise ValueError

        uuid = generate_key(user.user_id(), device_id)
        settings = UserSettings.query(ancestor = uuid).fetch()
        return settings[0]

    def _proximity_query(self, user, device_id):
        # Check if the parameters are valid
        if not user or not device_id:
            raise ValueError

        settings = self.retrieve_settings(user, device_id)
        location = self.retrieve_location(user, device_id)

        # TODO: filter by invisible property
        # Remove current point from query
        search_users = UserPosition.all()

        # Find all existing users within search_radius meters
        query_result = UserPosition.proximity_fetch(
                        search_users,
                        location.location,
                        max_results = 100,
                        max_distance = 9000) 
                        #max_distance = 1000) 
                        #max_distance = settings.search_radius) 

        return query_result

    def _format_query_result(self, query_result):
        formatted_answer = { 'response' : 'OK',
                             'users'    : [],
                           }

        for result in query_result:
            # Construct a hash with the user record 
            user_record = {}
            user_record['name']      = result.user.nickname()
            user_record['id']        = result.user.user_id()
            user_record['latitude']  = str(result._get_latitude())
            user_record['longitude'] = str(result._get_longitude())
            formatted_answer['users'].append(user_record)

        return formatted_answer

    def _format_answer(self, friend_name, latitude, longitude):
        friend = FriendLocation()
        friend.friend_name = friend_name
        friend.latitude    = latitude
        friend.longitude   = longitude
        return friend

    @endpoints.method(QueryRequestMessage, message_types.VoidMessage,
                      path='meetup_query', http_method='POST',
                      name='post_query')
    def post_query(self, request):
        try:
            user = users.get_current_user()
            if not user:
                auth_url = users.create_login_url(self.request.uri)
                return self.redirect(auth_url)

            current_user = endpoints.get_current_user()
            #if raise_unauthorized and current_user is None:
            #   raise endpoints.UnauthorizedException('Invalid token.')

            print "User is [%s] [%s]" % (str(user), str(current_user))
            #query_result = self._proximity_query(user, device_id)
            #result_json  = self._format_query_result(query_result)
            #self.response.headers['Content-Type'] = 'application/json'  
            #return self.response.out.write(json.dumps(result_json))
        except ValueError:
            return self.error(404)

        return message_types.VoidMessage()

    @endpoints.method(message_types.VoidMessage, QueryResponseMessage,
                      path='meetup_query', http_method='GET',
                      name='check_query')
    def check_query(self, unused_request):
        user = users.get_current_user()
        current_user = endpoints.get_current_user()
        print "User is [%s] [%s]" % (str(user), str(current_user))

        friend1 = self._format_answer("gigel", 20.123, 21.23)
        friend2 = self._format_answer("gogu", 22.23, 23.23)
 
        friends_list = [ friend1, friend2 ] 
        return QueryResponseMessage(friends=friends_list)

