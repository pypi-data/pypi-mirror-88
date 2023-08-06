import graphene

from .product import (
    CreateProduct, UpdateProduct, DeleteProduct)
from .product_file_path import (
    CreateProductFilePath, UpdateProductFilePath, DeleteProductFilePath)
from .product_type import (
    CreateProductType, UpdateProductType, DeleteProductType)
from .product_relation_type import (
    CreateProductRelationTypes, UpdateProductRelationType, DeleteProductRelationTypes)
from .product_relation import (
    CreateProductRelation, DeleteProductRelation)

from .auth import GitHubAuth, StoreAdminAppToken

from .query import Query

##__________________________________________________________________||
class Mutation(graphene.ObjectType):

    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()

    create_product_file_path = CreateProductFilePath.Field()
    update_product_file_path = UpdateProductFilePath.Field()
    delete_product_file_path = DeleteProductFilePath.Field()

    create_product_type = CreateProductType.Field()
    update_product_type = UpdateProductType.Field()
    delete_product_type = DeleteProductType.Field()

    create_product_relation_types = CreateProductRelationTypes.Field()
    update_product_relation_type = UpdateProductRelationType.Field()
    delete_product_relation_types = DeleteProductRelationTypes.Field()

    create_product_relation = CreateProductRelation.Field()
    delete_product_relation = DeleteProductRelation.Field()

    github_auth = GitHubAuth.Field()
    store_admin_app_token = StoreAdminAppToken.Field()

##__________________________________________________________________||
