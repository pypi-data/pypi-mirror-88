"""define filters

Define filters by using graphene-sqlalchemy-filter:
https://github.com/art1415926535/graphene-sqlalchemy-filter

example:
https://github.com/art1415926535/graphene-sqlalchemy-filter/blob/1.10.2/examples/clients_and_records/filters.py

"""
import graphene
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet

from ..models import Product as ProductModel
from ..models import ProductType as ProductTypeModel

##__________________________________________________________________||
class ProductFilter(FilterSet):
   type_name = graphene.String()

   class Meta:
       model = ProductModel
       fields = {
           'type_id': ['eq', ],
       }

   @staticmethod
   def type_name_filter(info, query, value):
       # "Filters that require join":
       # https://github.com/art1415926535/graphene-sqlalchemy-filter/tree/1.10.2#filters-that-require-join
       query = query.join(ProductTypeModel)
       filter_ = ProductTypeModel.name == value
       return query, filter_

class ProductTypeFilter(FilterSet):
   class Meta:
       model = ProductTypeModel
       fields = { }

##__________________________________________________________________||
class PFilterableConnectionField(FilterableConnectionField):
    filters = {
        ProductModel: ProductFilter(),
        ProductTypeModel: ProductTypeFilter()
    }

##__________________________________________________________________||
