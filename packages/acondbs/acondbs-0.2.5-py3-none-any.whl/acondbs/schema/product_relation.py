import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import Product as ProductModel
from ..models import ProductRelation as ProductRelationModel
from ..models import ProductRelationType as ProductRelationTypeModel

from ..db.sa import sa
from ..db.backup import request_backup_db

from .connection import CountedConnection
from .filter_ import PFilterableConnectionField

##__________________________________________________________________||
class ProductRelation(SQLAlchemyObjectType):
    '''A relation from one product to another'''
    class Meta:
        model = ProductRelationModel
        interfaces = (graphene.relay.Node, )
        connection_class = CountedConnection
        connection_field_factory = PFilterableConnectionField.factory

##__________________________________________________________________||
class CreateProductRelationInput(graphene.InputObjectType):
    '''An input to createProductRelation()'''
    type_id = graphene.Int(
        required=True,
        description=(
            'The typeId of the product relation type of the relation '
            'from "self" to the "other"'))
    self_product_id = graphene.Int(
        required=True,
        description=('The productId of the self product'))
    other_product_id = graphene.Int(
        required=True,
        description=('The productId of the other product'))

##__________________________________________________________________||
class CreateProductRelation(graphene.Mutation):
    '''Add relations between two products. The arguments only specify the relation
    from one product to the other. The reverse relation will be also added.

    '''
    class Arguments:
        input = CreateProductRelationInput(required=True)

    ok = graphene.Boolean()
    product_relation = graphene.Field(lambda: ProductRelation)

    def mutate(root, info, input):
        type_ = ProductRelationTypeModel.query.filter_by(type_id=input['type_id']).one()
        self_ = ProductModel.query.filter_by(product_id=input['self_product_id']).one()
        other = ProductModel.query.filter_by(product_id=input['other_product_id']).one()

        model = ProductRelationModel(type_=type_, self_=self_, other=other)

        sa.session.add(model)
        sa.session.commit()
        ok = True
        request_backup_db()
        return CreateProductRelation(product_relation=model, ok=ok)

class DeleteProductRelation(graphene.Mutation):
    '''Remove relations from two products.

    '''
    class Arguments:
        relation_id = graphene.Int(
            required=True,
            description=('The relationId of a relation. The reverse relation '
                         'will automatically be removed.'))

    ok = graphene.Boolean()

    def mutate(root, info, relation_id):
        model = ProductRelationModel.query.filter_by(relation_id=relation_id).one()
        sa.session.delete(model)
        sa.session.commit()
        ok = True
        request_backup_db()
        return DeleteProductRelation(ok=ok)

##__________________________________________________________________||
