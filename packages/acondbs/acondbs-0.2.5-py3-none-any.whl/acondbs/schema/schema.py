import graphene

from .query import Query
from .mutation import Mutation

##__________________________________________________________________||
def create_schema(enable_mutation=True):
    if enable_mutation:
        return graphene.Schema(query=Query, mutation=Mutation)
    return graphene.Schema(query=Query)

##__________________________________________________________________||
