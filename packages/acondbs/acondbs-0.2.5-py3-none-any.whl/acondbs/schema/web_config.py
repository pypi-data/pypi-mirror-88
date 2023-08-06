import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import WebConfig as WebConfigModel

from .connection import CountedConnection
from .filter_ import PFilterableConnectionField

##__________________________________________________________________||
class WebConfig(SQLAlchemyObjectType):
    '''Web configuration'''
    class Meta:
        model = WebConfigModel
        interfaces = (graphene.relay.Node, )
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory

##__________________________________________________________________||
