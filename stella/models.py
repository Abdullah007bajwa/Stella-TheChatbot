from neomodel import StructuredNode, StringProperty


class BotUsers(StructuredNode):
    name = StringProperty(max_length=100)
    gender = StringProperty(max_length=20)
    ipaddress = StringProperty(max_length=15)
    password = StringProperty(max_length=16)
    email = StringProperty(max_length=100)
    picture = StringProperty()
