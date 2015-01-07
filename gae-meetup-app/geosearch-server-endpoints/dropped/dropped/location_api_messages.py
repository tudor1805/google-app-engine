'''
@author: Tudor Cornea
@contact: tudor.cornea@gmail.com
'''

from protorpc import messages

class LocationRequestMessage(messages.Message):
    """ProtoRPC message definition to represent a Location request."""
    device_id = messages.StringField(1, required=True)
    latitude  = messages.FloatField(2,  required=True)
    longitude = messages.FloatField(3,  required=True)

class LocationResponseMessage(messages.Message):
    """ProtoRPC message definition to represent a Location response."""
    msg       = messages.StringField(1)

