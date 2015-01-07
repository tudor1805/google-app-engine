'''
@author: Tudor Cornea
@contact: tudor.cornea@gmail.com
'''

from protorpc import messages

"""==== Settings API ===="""
class SettingsRequestMessage(messages.Message):
    user_id       = messages.StringField(1,  required=True)
    device_id     = messages.StringField(2,  required=True)
    search_radius = messages.IntegerField(3, required=True)
    is_visible    = messages.BooleanField(4, required=True)

"""==== Location API ===="""
class LocationRequestMessage(messages.Message):
    user_id   = messages.StringField(1,  required=True)
    device_id = messages.StringField(2,  required=True)
    latitude  = messages.FloatField(3,   required=True)
    longitude = messages.FloatField(4,   required=True)

"""==== Query API ===="""
class FriendLocation(messages.Message):
    user_friend_id = messages.StringField(1)
    latitude       = messages.FloatField(2)
    longitude      = messages.FloatField(3)

class QueryRequestMessage(messages.Message):
    user_id         = messages.StringField(1, required=True)
    device_id       = messages.StringField(2, required=True)
    user_friend_ids = messages.StringField(3, repeated=True)

class QueryResponseMessage(messages.Message):
    near_friends = messages.MessageField(FriendLocation, 1, repeated=True)

