from flask import current_app
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphql import GraphQLError

from .product import Product, ProductModel
from .product_file_path import ProductFilePath, ProductFilePathModel
from .product_type import ProductType, ProductTypeModel
from .product_relation_type import ProductRelationType, ProductRelationTypeModel
from .product_relation import ProductRelation, ProductRelationModel

from .web_config import WebConfig

from .filter_ import PFilterableConnectionField

from .auth import OAuthAppInfo, GitHubUser

from ..misc import githubauth

##__________________________________________________________________||
class Query(graphene.ObjectType):

    version = graphene.String()

    def resolve_version(self, info):
        from .. import __version__
        return __version__

    node = relay.Node.Field()

    web_config = graphene.Field(WebConfig)

    def resolve_web_config(self, info, **kwargs):
        return WebConfig.get_query(info).one_or_none()

    all_product_types = PFilterableConnectionField(ProductType.connection)

    product_type = graphene.Field(ProductType, type_id=graphene.Int(), name=graphene.String())

    def resolve_product_type(self, info, **kwargs):
        filter = [getattr(ProductTypeModel, k)==v for k, v in kwargs.items()]
        # e.g., [ProductTypeModel.type_id == 1, ProductTypeModel.name == 'map']

        return ProductType.get_query(info).filter(*filter).one_or_none()

    all_products = PFilterableConnectionField(Product.connection)
    all_product_file_paths = PFilterableConnectionField(ProductFilePath.connection)

    product = graphene.Field(
        Product,
        product_id=graphene.Int(),
        type_id=graphene.Int(),
        name=graphene.String())

    def resolve_product(self, info, **kwargs):

        filter = [getattr(ProductModel, k)==v for k, v in kwargs.items()]
        # e.g., [ProductModel.type_id == 1, ProductModel.name == 'map_001']

        return Product.get_query(info).filter(*filter).one_or_none()

    all_product_relation_types = PFilterableConnectionField(ProductRelationType.connection)

    product_relation_type = graphene.Field(ProductRelationType, type_id=graphene.Int(), name=graphene.String())

    def resolve_product_relation_type(self, info, **kwargs):
        filter = [getattr(ProductRelationTypeModel, k)==v for k, v in kwargs.items()]
        return ProductRelationType.get_query(info).filter(*filter).one_or_none()

    all_product_relations = PFilterableConnectionField(ProductRelation.connection)

    product_relation = graphene.Field(ProductRelation, relation_id=graphene.Int())

    def resolve_product_relation(self, info, **kwargs):
        filter = [getattr(ProductRelationModel, k)==v for k, v in kwargs.items()]
        return ProductRelation.get_query(info).filter(*filter).one_or_none()

    github_user = graphene.Field(GitHubUser)

    def resolve_github_user(self, info):

        auth = info.context.headers.get('Authorization')
        # e.g., 'Bearer "xxxx"'

        if not auth:
            raise GraphQLError('Authorization is required')

        token = auth.split()[1].strip('"')
        # e.g., "xxxx"

        user = githubauth.get_user(token)
        if not user:
            raise GraphQLError('Unsuccessful to obtain the user')

        return GitHubUser(**user);

    oauth_app_info = graphene.Field(
        OAuthAppInfo,
        admin=graphene.Boolean(default_value=False)
        )

    def resolve_oauth_app_info(self, info, admin):
        print(admin)
        if admin:
            return OAuthAppInfo(
                client_id=current_app.config['GITHUB_AUTH_ADMIN_CLIENT_ID'],
                authorize_url=current_app.config['GITHUB_AUTH_AUTHORIZE_URL'],
                token_url=current_app.config['GITHUB_AUTH_TOKEN_URL'],
                redirect_uri=current_app.config['GITHUB_AUTH_ADMIN_REDIRECT_URI']
            )

        return OAuthAppInfo(
            client_id=current_app.config['GITHUB_AUTH_CLIENT_ID'],
            authorize_url=current_app.config['GITHUB_AUTH_AUTHORIZE_URL'],
            token_url=current_app.config['GITHUB_AUTH_TOKEN_URL'],
            redirect_uri=current_app.config['GITHUB_AUTH_REDIRECT_URI']
        )
##__________________________________________________________________||
