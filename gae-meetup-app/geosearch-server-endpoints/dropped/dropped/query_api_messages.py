'''
@author: Tudor Cornea
@contact: tudor.cornea@gmail.com
'''

from protorpc import messages

class FriendLocation(messages.Message):
    friend_name = messages.StringField(1)
    latitude    = messages.FloatField(2)
    longitude   = messages.FloatField(3)

class QueryRequestMessage(messages.Message):
    """ProtoRPC message definition to represent a Query request."""
    friends = messages.StringField(1, repeated=True)

class QueryResponseMessage(messages.Message):
    """ProtoRPC message definition to represent a Query response."""
    friends = messages.MessageField(FriendLocation, 1, repeated=True)

