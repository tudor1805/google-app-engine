'''
@author: Tudor Cornea
@contact: tudor.cornea@gmail.com
'''

import webapp2

import os

import endpoints
from protorpc import *

from api.settings_api_messages import SettingsRequestMessage
from api.settings_api_messages import SettingsResponseMessage

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import db

from models.user_settings import *

# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'                                                                                                     
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

package = 'MeetUpSettings'

@endpoints.api(name='meetup_settings', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID,
                                   ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE])
class SettingsApi(remote.Service):
    """ MeetUp Settings API v1."""

    def _retrieve_settings(self, user, device_id):
        # Check if the parameters are valid
        if not user or not device_id:
            raise ValueError

        uuid = generate_key(user.user_id(), device_id)
        settings = UserSettings.query(ancestor = uuid).fetch()
        return settings[0]

    def _update_settings(self, user, device_id, search_radius, visible):
        # Check if the parameters are valid
        if not user or not device_id or not search_radius:
            raise ValueError

        uuid = generate_key(user.user_id(), device_id)

        # Delete any existing settings
        ndb.delete_multi(
            UserSettings.query(ancestor = uuid).fetch(keys_only=True)
        )

        # Create the new settings
        setting = UserSettings(parent = uuid)
        setting.user = user
        setting.device = device_id
        setting.search_radius = search_radius
        setting.visible = visible
        setting.put()

    @endpoints.method(SettingsRequestMessage, message_types.VoidMessage,
                      path='meetup_settings', http_method='POST',
                      name='update_settings')
    def update_settings(self, request):
        try:
            user = users.get_current_user()
            if not user:
                auth_url = users.create_login_url(self.request.uri)
                return self.redirect(auth_url)

            #self._update_settings(user, request.device_id,
            #                      request.search_radius, request.is_visible)
            print "User is [%s]" % str(user)
        except ValueError:
            return self.error(400)

        return message_types.VoidMessage()

    @endpoints.method(message_types.VoidMessage, SettingsResponseMessage,
                      path='meetup_settings', http_method='GET',
                      name='retrieve_settings')
    def retrieve_settings(self, unused_request):
        return SettingsResponseMessage(msg = "Not Implemented !")


