'''
@author: Tudor Cornea
@contact: tudor.cornea@gmail.com
'''

from protorpc import messages

class SettingsRequestMessage(messages.Message):
    """ProtoRPC message definition to represent a Settings request."""
    device_id     = messages.StringField(1,  required=True)
    search_radius = messages.IntegerField(2, required=True)
    is_visible    = messages.BooleanField(3, required=True)

class SettingsResponseMessage(messages.Message):
    """ProtoRPC message definition to represent a Settings response."""
    msg           = messages.StringField(1)

