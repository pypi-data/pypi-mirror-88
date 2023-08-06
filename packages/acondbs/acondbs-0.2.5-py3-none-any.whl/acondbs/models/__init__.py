"""declare ORM models

In this packages, ORM (Object-relational mapping) models are declared.
One model is mapped to one table in the DB. Models are declared as
Python classes inheriting the Model class in Flask-SQLAlchemy.

"Declaring Models" in Flask-SQLAlchemy doc:
https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

"Declare a Mapping" in SQLAlchemy doc:
https://docs.sqlalchemy.org/en/13/orm/tutorial.html#declare-a-mapping

"""

##__________________________________________________________________||
from .product_type import ProductType
from .product import Product
from .product_file_path import ProductFilePath
from .product_relation_type import ProductRelationType
from .product_relation import ProductRelation

from .web_config import WebConfig

from .admin_app_token import AdminAppToken

##__________________________________________________________________||
