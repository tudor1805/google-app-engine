'''
@author: Tudor Cornea
@contact: tudor.cornea@gmail.com
'''

import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

from models.user_position import *
from models.user_settings import *

from pprint import pprint

class Tester(webapp2.RequestHandler):

    def empty_locations(self):
        # Delete any existing location settings
        existing_locations = UserPosition.all()

        for user_position in existing_locations:
             user_position.delete()

    def empty_settings(self):
        # Delete any existing settings
        ndb.delete_multi(
            UserSettings.query().fetch(keys_only=True)
        )

    def create_settings_record(self, user, device_id, search_radius, visible):
        # Check if the parameters are valid
        if not user or not device_id or not search_radius:
            raise ValueError

        uuid = generate_key(user.user_id(), device_id)

        # Create the new settings
        setting = UserSettings(parent = uuid)
        setting.user = user
        setting.device = device_id
        setting.search_radius = search_radius
        setting.visible = visible
        setting.put()

    def create_location_record(self, user, device_id, location):
        # Check if the parameters are valid
        if not user or not device_id or not location:
            raise ValueError

        # Store the new location
        user_pos = UserPosition(location = location,
                                user = user,
                                device = device_id)
        user_pos.update_location()
        user_pos.put()

    def get(self):
        user = users.get_current_user()
        if not user:
            auth_url = users.create_login_url(self.request.uri)
            return self.redirect(auth_url)

        # Perform cleanup
        self.empty_locations()
        self.empty_settings()

        # Create settings
        self.create_settings_record(user, 'device1', 150,  True)
        self.create_settings_record(user, 'device1', 150,  True)
        self.create_settings_record(user, 'device2', 300,  True)
        self.create_settings_record(user, 'device3', 500,  False)
        self.create_settings_record(user, 'device4', 10000, True)
        self.create_settings_record(user, 'device5', 100,  True)
        self.create_settings_record(user, 'device6', 100,  True)

        # Create locations 
        self.create_location_record(user, 'device1', db.GeoPt(43.80746, 28.58187))
        self.create_location_record(user, 'device2', db.GeoPt(43.80768, 28.57233))
        self.create_location_record(user, 'device3', db.GeoPt(43.81948, 28.58823))
        self.create_location_record(user, 'device4', db.GeoPt(43.85958, 28.57578))
        self.create_location_record(user, 'device5', db.GeoPt(44.17256, 28.63664))
        self.create_location_record(user, 'device6', db.GeoPt(44.13783, 28.62089))

        self.response.write("Ok")

