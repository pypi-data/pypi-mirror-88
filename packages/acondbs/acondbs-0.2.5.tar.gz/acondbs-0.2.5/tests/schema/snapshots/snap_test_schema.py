# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_types 1'] = {
    'data': {
        '__schema': {
            'types': [
                {
                    'description': None,
                    'fields': [
                        {
                            'description': None,
                            'name': 'version',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': 'The ID of the object',
                            'name': 'node',
                            'type': {
                                'name': 'Node'
                            }
                        },
                        {
                            'description': None,
                            'name': 'webConfig',
                            'type': {
                                'name': 'WebConfig'
                            }
                        },
                        {
                            'description': None,
                            'name': 'allProductTypes',
                            'type': {
                                'name': 'ProductTypeConnection'
                            }
                        },
                        {
                            'description': None,
                            'name': 'productType',
                            'type': {
                                'name': 'ProductType'
                            }
                        },
                        {
                            'description': None,
                            'name': 'allProducts',
                            'type': {
                                'name': 'ProductConnection'
                            }
                        },
                        {
                            'description': None,
                            'name': 'allProductFilePaths',
                            'type': {
                                'name': 'ProductFilePathConnection'
                            }
                        },
                        {
                            'description': None,
                            'name': 'product',
                            'type': {
                                'name': 'Product'
                            }
                        },
                        {
                            'description': None,
                            'name': 'allProductRelationTypes',
                            'type': {
                                'name': 'ProductRelationTypeConnection'
                            }
                        },
                        {
                            'description': None,
                            'name': 'productRelationType',
                            'type': {
                                'name': 'ProductRelationType'
                            }
                        },
                        {
                            'description': None,
                            'name': 'allProductRelations',
                            'type': {
                                'name': 'ProductRelationConnection'
                            }
                        },
                        {
                            'description': None,
                            'name': 'productRelation',
                            'type': {
                                'name': 'ProductRelation'
                            }
                        },
                        {
                            'description': None,
                            'name': 'githubUser',
                            'type': {
                                'name': 'GitHubUser'
                            }
                        },
                        {
                            'description': None,
                            'name': 'oauthAppInfo',
                            'type': {
                                'name': 'OAuthAppInfo'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'Query'
                },
                {
                    'description': 'The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.',
                    'fields': None,
                    'inputFields': None,
                    'name': 'String'
                },
                {
                    'description': 'An object with an ID',
                    'fields': [
                        {
                            'description': 'The ID of the object.',
                            'name': 'id',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'Node'
                },
                {
                    'description': 'The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.',
                    'fields': None,
                    'inputFields': None,
                    'name': 'ID'
                },
                {
                    'description': 'Web configuration',
                    'fields': [
                        {
                            'description': None,
                            'name': 'configId',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'headTitle',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'toolbarTitle',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'devtoolLoadingstate',
                            'type': {
                                'name': 'Boolean'
                            }
                        },
                        {
                            'description': None,
                            'name': 'productCreationDialog',
                            'type': {
                                'name': 'Boolean'
                            }
                        },
                        {
                            'description': None,
                            'name': 'productUpdateDialog',
                            'type': {
                                'name': 'Boolean'
                            }
                        },
                        {
                            'description': None,
                            'name': 'productDeletionDialog',
                            'type': {
                                'name': 'Boolean'
                            }
                        },
                        {
                            'description': 'The ID of the object.',
                            'name': 'id',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'WebConfig'
                },
                {
                    'description': 'The `Boolean` scalar type represents `true` or `false`.',
                    'fields': None,
                    'inputFields': None,
                    'name': 'Boolean'
                },
                {
                    'description': None,
                    'fields': [
                        {
                            'description': 'Pagination data for this connection.',
                            'name': 'pageInfo',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': 'Contains the nodes in this connection.',
                            'name': 'edges',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'totalCount',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'ProductTypeConnection'
                },
                {
                    'description': 'The Relay compliant `PageInfo` type, containing data necessary to paginate this connection.',
                    'fields': [
                        {
                            'description': 'When paginating forwards, are there more items?',
                            'name': 'hasNextPage',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': 'When paginating backwards, are there more items?',
                            'name': 'hasPreviousPage',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': 'When paginating backwards, the cursor to continue.',
                            'name': 'startCursor',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': 'When paginating forwards, the cursor to continue.',
                            'name': 'endCursor',
                            'type': {
                                'name': 'String'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'PageInfo'
                },
                {
                    'description': 'A Relay edge containing a `ProductType` and its cursor.',
                    'fields': [
                        {
                            'description': 'The item at the end of the edge',
                            'name': 'node',
                            'type': {
                                'name': 'ProductType'
                            }
                        },
                        {
                            'description': 'A cursor for use in pagination',
                            'name': 'cursor',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'ProductTypeEdge'
                },
                {
                    'description': 'A product type',
                    'fields': [
                        {
                            'description': None,
                            'name': 'typeId',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'name',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'order',
                            'type': {
                                'name': 'Int'
                            }
                        },
                        {
                            'description': None,
                            'name': 'indefArticle',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'singular',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'plural',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'icon',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'products',
                            'type': {
                                'name': 'ProductConnection'
                            }
                        },
                        {
                            'description': 'The ID of the object.',
                            'name': 'id',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'ProductType'
                },
                {
                    'description': 'The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31 - 1) and 2^31 - 1 since represented in JSON as double-precision floating point numbers specifiedby [IEEE 754](http://en.wikipedia.org/wiki/IEEE_floating_point).',
                    'fields': None,
                    'inputFields': None,
                    'name': 'Int'
                },
                {
                    'description': None,
                    'fields': [
                        {
                            'description': 'Pagination data for this connection.',
                            'name': 'pageInfo',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': 'Contains the nodes in this connection.',
                            'name': 'edges',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'totalCount',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'ProductConnection'
                },
                {
                    'description': 'A Relay edge containing a `Product` and its cursor.',
                    'fields': [
                        {
                            'description': 'The item at the end of the edge',
                            'name': 'node',
                            'type': {
                                'name': 'Product'
                            }
                        },
                        {
                            'description': 'A cursor for use in pagination',
                            'name': 'cursor',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'ProductEdge'
                },
                {
                    'description': None,
                    'fields': [
                        {
                            'description': None,
                            'name': 'productId',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'typeId',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'name',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'contact',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'dateProduced',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'producedBy',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'datePosted',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'postedBy',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'dateUpdated',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'updatedBy',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'note',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'type_',
                            'type': {
                                'name': 'ProductType'
                            }
                        },
                        {
                            'description': None,
                            'name': 'paths',
                            'type': {
                                'name': 'ProductFilePathConnection'
                            }
                        },
                        {
                            'description': None,
                            'name': 'relations',
                            'type': {
                                'name': 'ProductRelationConnection'
                            }
                        },
                        {
                            'description': 'The ID of the object.',
                            'name': 'id',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'Product'
                },
                {
                    'description': None,
                    'fields': [
                        {
                            'description': 'Pagination data for this connection.',
                            'name': 'pageInfo',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': 'Contains the nodes in this connection.',
                            'name': 'edges',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'totalCount',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'ProductFilePathConnection'
                },
                {
                    'description': 'A Relay edge containing a `ProductFilePath` and its cursor.',
                    'fields': [
                        {
                            'description': 'The item at the end of the edge',
                            'name': 'node',
                            'type': {
                                'name': 'ProductFilePath'
                            }
                        },
                        {
                            'description': 'A cursor for use in pagination',
                            'name': 'cursor',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'ProductFilePathEdge'
                },
                {
                    'description': None,
                    'fields': [
                        {
                            'description': None,
                            'name': 'pathId',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'path',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'note',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'productId',
                            'type': {
                                'name': 'Int'
                            }
                        },
                        {
                            'description': None,
                            'name': 'product',
                            'type': {
                                'name': 'Product'
                            }
                        },
                        {
                            'description': 'The ID of the object.',
                            'name': 'id',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'ProductFilePath'
                },
                {
                    'description': 'An enumeration.',
                    'fields': None,
                    'inputFields': None,
                    'name': 'ProductFilePathSortEnum'
                },
                {
                    'description': None,
                    'fields': [
                        {
                            'description': 'Pagination data for this connection.',
                            'name': 'pageInfo',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': 'Contains the nodes in this connection.',
                            'name': 'edges',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'totalCount',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'ProductRelationConnection'
                },
                {
                    'description': 'A Relay edge containing a `ProductRelation` and its cursor.',
                    'fields': [
                        {
                            'description': 'The item at the end of the edge',
                            'name': 'node',
                            'type': {
                                'name': 'ProductRelation'
                            }
                        },
                        {
                            'description': 'A cursor for use in pagination',
                            'name': 'cursor',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'ProductRelationEdge'
                },
                {
                    'description': 'A relation from one product to another',
                    'fields': [
                        {
                            'description': None,
                            'name': 'relationId',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'typeId',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'selfProductId',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'otherProductId',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'reverseRelationId',
                            'type': {
                                'name': 'Int'
                            }
                        },
                        {
                            'description': None,
                            'name': 'type_',
                            'type': {
                                'name': 'ProductRelationType'
                            }
                        },
                        {
                            'description': None,
                            'name': 'self_',
                            'type': {
                                'name': 'Product'
                            }
                        },
                        {
                            'description': None,
                            'name': 'other',
                            'type': {
                                'name': 'Product'
                            }
                        },
                        {
                            'description': None,
                            'name': 'reverse',
                            'type': {
                                'name': 'ProductRelation'
                            }
                        },
                        {
                            'description': 'The ID of the object.',
                            'name': 'id',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'ProductRelation'
                },
                {
                    'description': 'A type of relations between products',
                    'fields': [
                        {
                            'description': None,
                            'name': 'typeId',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'name',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'reverseTypeId',
                            'type': {
                                'name': 'Int'
                            }
                        },
                        {
                            'description': None,
                            'name': 'indefArticle',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'singular',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'plural',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'reverse',
                            'type': {
                                'name': 'ProductRelationType'
                            }
                        },
                        {
                            'description': None,
                            'name': 'relations',
                            'type': {
                                'name': 'ProductRelationConnection'
                            }
                        },
                        {
                            'description': 'The ID of the object.',
                            'name': 'id',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'ProductRelationType'
                },
                {
                    'description': 'An enumeration.',
                    'fields': None,
                    'inputFields': None,
                    'name': 'ProductRelationSortEnum'
                },
                {
                    'description': None,
                    'fields': None,
                    'inputFields': [
                        {
                            'defaultValue': None,
                            'description': 'Exact match.',
                            'name': 'typeId'
                        },
                        {
                            'defaultValue': None,
                            'description': 'Conjunction of filters joined by ``AND``.',
                            'name': 'and'
                        },
                        {
                            'defaultValue': None,
                            'description': 'Conjunction of filters joined by ``OR``.',
                            'name': 'or'
                        },
                        {
                            'defaultValue': None,
                            'description': 'Negation of filters.',
                            'name': 'not'
                        },
                        {
                            'defaultValue': None,
                            'description': None,
                            'name': 'typeName'
                        }
                    ],
                    'name': 'ProductFilter'
                },
                {
                    'description': 'An enumeration.',
                    'fields': None,
                    'inputFields': None,
                    'name': 'ProductSortEnum'
                },
                {
                    'description': None,
                    'fields': None,
                    'inputFields': [
                        {
                            'defaultValue': None,
                            'description': 'Conjunction of filters joined by ``AND``.',
                            'name': 'and'
                        },
                        {
                            'defaultValue': None,
                            'description': 'Conjunction of filters joined by ``OR``.',
                            'name': 'or'
                        },
                        {
                            'defaultValue': None,
                            'description': 'Negation of filters.',
                            'name': 'not'
                        }
                    ],
                    'name': 'ProductTypeFilter'
                },
                {
                    'description': 'An enumeration.',
                    'fields': None,
                    'inputFields': None,
                    'name': 'ProductTypeSortEnum'
                },
                {
                    'description': None,
                    'fields': [
                        {
                            'description': 'Pagination data for this connection.',
                            'name': 'pageInfo',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': 'Contains the nodes in this connection.',
                            'name': 'edges',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'totalCount',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'ProductRelationTypeConnection'
                },
                {
                    'description': 'A Relay edge containing a `ProductRelationType` and its cursor.',
                    'fields': [
                        {
                            'description': 'The item at the end of the edge',
                            'name': 'node',
                            'type': {
                                'name': 'ProductRelationType'
                            }
                        },
                        {
                            'description': 'A cursor for use in pagination',
                            'name': 'cursor',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'ProductRelationTypeEdge'
                },
                {
                    'description': 'An enumeration.',
                    'fields': None,
                    'inputFields': None,
                    'name': 'ProductRelationTypeSortEnum'
                },
                {
                    'description': None,
                    'fields': [
                        {
                            'description': None,
                            'name': 'login',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'name',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'avatarUrl',
                            'type': {
                                'name': 'String'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'GitHubUser'
                },
                {
                    'description': None,
                    'fields': [
                        {
                            'description': None,
                            'name': 'clientId',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'authorizeUrl',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'tokenUrl',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'redirectUri',
                            'type': {
                                'name': 'String'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'OAuthAppInfo'
                },
                {
                    'description': None,
                    'fields': [
                        {
                            'description': 'Create a product',
                            'name': 'createProduct',
                            'type': {
                                'name': 'CreateProduct'
                            }
                        },
                        {
                            'description': '''Update a product. Note: This is to update the DB entry about a product. If the
product itself has been updated, a new entry should be added by
createProduct()''',
                            'name': 'updateProduct',
                            'type': {
                                'name': 'UpdateProduct'
                            }
                        },
                        {
                            'description': 'Delete a product',
                            'name': 'deleteProduct',
                            'type': {
                                'name': 'DeleteProduct'
                            }
                        },
                        {
                            'description': None,
                            'name': 'createProductFilePath',
                            'type': {
                                'name': 'CreateProductFilePath'
                            }
                        },
                        {
                            'description': None,
                            'name': 'updateProductFilePath',
                            'type': {
                                'name': 'UpdateProductFilePath'
                            }
                        },
                        {
                            'description': None,
                            'name': 'deleteProductFilePath',
                            'type': {
                                'name': 'DeleteProductFilePath'
                            }
                        },
                        {
                            'description': 'Create a product type',
                            'name': 'createProductType',
                            'type': {
                                'name': 'CreateProductType'
                            }
                        },
                        {
                            'description': 'Update a product type',
                            'name': 'updateProductType',
                            'type': {
                                'name': 'UpdateProductType'
                            }
                        },
                        {
                            'description': 'Delete a product type',
                            'name': 'deleteProductType',
                            'type': {
                                'name': 'DeleteProductType'
                            }
                        },
                        {
                            'description': 'Create a pair of product relation types',
                            'name': 'createProductRelationTypes',
                            'type': {
                                'name': 'CreateProductRelationTypes'
                            }
                        },
                        {
                            'description': 'Update a product relation type',
                            'name': 'updateProductRelationType',
                            'type': {
                                'name': 'UpdateProductRelationType'
                            }
                        },
                        {
                            'description': 'Delete a pair of product relation types',
                            'name': 'deleteProductRelationTypes',
                            'type': {
                                'name': 'DeleteProductRelationTypes'
                            }
                        },
                        {
                            'description': '''Add relations between two products. The arguments only specify the relation
from one product to the other. The reverse relation will be also added.''',
                            'name': 'createProductRelation',
                            'type': {
                                'name': 'CreateProductRelation'
                            }
                        },
                        {
                            'description': '''Remove relations from two products.

    ''',
                            'name': 'deleteProductRelation',
                            'type': {
                                'name': 'DeleteProductRelation'
                            }
                        },
                        {
                            'description': None,
                            'name': 'githubAuth',
                            'type': {
                                'name': 'GitHubAuth'
                            }
                        },
                        {
                            'description': None,
                            'name': 'storeAdminAppToken',
                            'type': {
                                'name': 'StoreAdminAppToken'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'Mutation'
                },
                {
                    'description': 'Create a product',
                    'fields': [
                        {
                            'description': None,
                            'name': 'ok',
                            'type': {
                                'name': 'Boolean'
                            }
                        },
                        {
                            'description': None,
                            'name': 'product',
                            'type': {
                                'name': 'Product'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'CreateProduct'
                },
                {
                    'description': 'Input to createProduct()',
                    'fields': None,
                    'inputFields': [
                        {
                            'defaultValue': None,
                            'description': 'A person or group that can be contacted for questions or issues about the product.',
                            'name': 'contact'
                        },
                        {
                            'defaultValue': None,
                            'description': 'Note about the product in MarkDown.',
                            'name': 'note'
                        },
                        {
                            'defaultValue': None,
                            'description': 'Paths to the products. e.g., nersc:/go/to/my/product_v3',
                            'name': 'paths'
                        },
                        {
                            'defaultValue': None,
                            'description': 'Relations to other products',
                            'name': 'relations'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The product type ID',
                            'name': 'typeId'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The name of the product',
                            'name': 'name'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The date on which the product was produced',
                            'name': 'dateProduced'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The person or group that produced the product',
                            'name': 'producedBy'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The person who entered the DB entry.',
                            'name': 'postedBy'
                        }
                    ],
                    'name': 'CreateProductInput'
                },
                {
                    'description': 'A relation to another product',
                    'fields': None,
                    'inputFields': [
                        {
                            'defaultValue': None,
                            'description': 'The product ID of the other product',
                            'name': 'productId'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The relation type ID',
                            'name': 'typeId'
                        }
                    ],
                    'name': 'RelationInputFields'
                },
                {
                    'description': '''The `Date` scalar type represents a Date
value as specified by
[iso8601](https://en.wikipedia.org/wiki/ISO_8601).''',
                    'fields': None,
                    'inputFields': None,
                    'name': 'Date'
                },
                {
                    'description': '''Update a product. Note: This is to update the DB entry about a product. If the
product itself has been updated, a new entry should be added by
createProduct()''',
                    'fields': [
                        {
                            'description': None,
                            'name': 'ok',
                            'type': {
                                'name': 'Boolean'
                            }
                        },
                        {
                            'description': None,
                            'name': 'product',
                            'type': {
                                'name': 'Product'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'UpdateProduct'
                },
                {
                    'description': 'Input to updateProduct()',
                    'fields': None,
                    'inputFields': [
                        {
                            'defaultValue': None,
                            'description': 'A person or group that can be contacted for questions or issues about the product.',
                            'name': 'contact'
                        },
                        {
                            'defaultValue': None,
                            'description': 'Note about the product in MarkDown.',
                            'name': 'note'
                        },
                        {
                            'defaultValue': None,
                            'description': 'Paths to the products. e.g., nersc:/go/to/my/product_v3',
                            'name': 'paths'
                        },
                        {
                            'defaultValue': None,
                            'description': 'Relations to other products',
                            'name': 'relations'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The person who updated the DB entry.',
                            'name': 'updatedBy'
                        }
                    ],
                    'name': 'UpdateProductInput'
                },
                {
                    'description': 'Delete a product',
                    'fields': [
                        {
                            'description': None,
                            'name': 'ok',
                            'type': {
                                'name': 'Boolean'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'DeleteProduct'
                },
                {
                    'description': None,
                    'fields': [
                        {
                            'description': None,
                            'name': 'ok',
                            'type': {
                                'name': 'Boolean'
                            }
                        },
                        {
                            'description': None,
                            'name': 'productFilePath',
                            'type': {
                                'name': 'ProductFilePath'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'CreateProductFilePath'
                },
                {
                    'description': None,
                    'fields': None,
                    'inputFields': [
                        {
                            'defaultValue': None,
                            'description': None,
                            'name': 'path'
                        },
                        {
                            'defaultValue': None,
                            'description': None,
                            'name': 'note'
                        },
                        {
                            'defaultValue': None,
                            'description': None,
                            'name': 'productId'
                        }
                    ],
                    'name': 'CreateProductFilePathInput'
                },
                {
                    'description': None,
                    'fields': [
                        {
                            'description': None,
                            'name': 'ok',
                            'type': {
                                'name': 'Boolean'
                            }
                        },
                        {
                            'description': None,
                            'name': 'productFilePath',
                            'type': {
                                'name': 'ProductFilePath'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'UpdateProductFilePath'
                },
                {
                    'description': None,
                    'fields': None,
                    'inputFields': [
                        {
                            'defaultValue': None,
                            'description': None,
                            'name': 'path'
                        },
                        {
                            'defaultValue': None,
                            'description': None,
                            'name': 'note'
                        }
                    ],
                    'name': 'UpdateProductFilePathInput'
                },
                {
                    'description': None,
                    'fields': [
                        {
                            'description': None,
                            'name': 'ok',
                            'type': {
                                'name': 'Boolean'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'DeleteProductFilePath'
                },
                {
                    'description': 'Create a product type',
                    'fields': [
                        {
                            'description': None,
                            'name': 'ok',
                            'type': {
                                'name': 'Boolean'
                            }
                        },
                        {
                            'description': None,
                            'name': 'productType',
                            'type': {
                                'name': 'ProductType'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'CreateProductType'
                },
                {
                    'description': 'Input to createProductType()',
                    'fields': None,
                    'inputFields': [
                        {
                            'defaultValue': None,
                            'description': 'The order in which the type is displayed, for example, in navigation bars.',
                            'name': 'order'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The indefinite article placed before the singular noun "i.e., "a" or "an". ',
                            'name': 'indefArticle'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The singular noun, the product type name in singular.',
                            'name': 'singular'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The plural noun, the product type name in plural.',
                            'name': 'plural'
                        },
                        {
                            'defaultValue': None,
                            'description': 'A name of the icon from https://materialdesignicons.com/',
                            'name': 'icon'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The name of the product type',
                            'name': 'name'
                        }
                    ],
                    'name': 'CreateProductTypeInput'
                },
                {
                    'description': 'Update a product type',
                    'fields': [
                        {
                            'description': None,
                            'name': 'ok',
                            'type': {
                                'name': 'Boolean'
                            }
                        },
                        {
                            'description': None,
                            'name': 'productType',
                            'type': {
                                'name': 'ProductType'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'UpdateProductType'
                },
                {
                    'description': 'Input to updateProductType()',
                    'fields': None,
                    'inputFields': [
                        {
                            'defaultValue': None,
                            'description': 'The order in which the type is displayed, for example, in navigation bars.',
                            'name': 'order'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The indefinite article placed before the singular noun "i.e., "a" or "an". ',
                            'name': 'indefArticle'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The singular noun, the product type name in singular.',
                            'name': 'singular'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The plural noun, the product type name in plural.',
                            'name': 'plural'
                        },
                        {
                            'defaultValue': None,
                            'description': 'A name of the icon from https://materialdesignicons.com/',
                            'name': 'icon'
                        }
                    ],
                    'name': 'UpdateProductTypeInput'
                },
                {
                    'description': 'Delete a product type',
                    'fields': [
                        {
                            'description': None,
                            'name': 'ok',
                            'type': {
                                'name': 'Boolean'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'DeleteProductType'
                },
                {
                    'description': 'Create a pair of product relation types',
                    'fields': [
                        {
                            'description': None,
                            'name': 'ok',
                            'type': {
                                'name': 'Boolean'
                            }
                        },
                        {
                            'description': None,
                            'name': 'productRelationType',
                            'type': {
                                'name': 'ProductRelationType'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'CreateProductRelationTypes'
                },
                {
                    'description': 'An input to createProductRelationTypes()',
                    'fields': None,
                    'inputFields': [
                        {
                            'defaultValue': None,
                            'description': 'The indefinite article placed before the singular noun "i.e., "a" or "an". ',
                            'name': 'indefArticle'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The singular noun, the relation type name in singular.',
                            'name': 'singular'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The plural noun, the relation type name in plural.',
                            'name': 'plural'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The name of the relation type',
                            'name': 'name'
                        }
                    ],
                    'name': 'CreateProductRelationTypeInput'
                },
                {
                    'description': 'Update a product relation type',
                    'fields': [
                        {
                            'description': None,
                            'name': 'ok',
                            'type': {
                                'name': 'Boolean'
                            }
                        },
                        {
                            'description': None,
                            'name': 'productRelationType',
                            'type': {
                                'name': 'ProductRelationType'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'UpdateProductRelationType'
                },
                {
                    'description': 'An input to updateProductRelationType()',
                    'fields': None,
                    'inputFields': [
                        {
                            'defaultValue': None,
                            'description': 'The indefinite article placed before the singular noun "i.e., "a" or "an". ',
                            'name': 'indefArticle'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The singular noun, the relation type name in singular.',
                            'name': 'singular'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The plural noun, the relation type name in plural.',
                            'name': 'plural'
                        }
                    ],
                    'name': 'UpdateProductRelationTypeInput'
                },
                {
                    'description': 'Delete a pair of product relation types',
                    'fields': [
                        {
                            'description': None,
                            'name': 'ok',
                            'type': {
                                'name': 'Boolean'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'DeleteProductRelationTypes'
                },
                {
                    'description': '''Add relations between two products. The arguments only specify the relation
from one product to the other. The reverse relation will be also added.''',
                    'fields': [
                        {
                            'description': None,
                            'name': 'ok',
                            'type': {
                                'name': 'Boolean'
                            }
                        },
                        {
                            'description': None,
                            'name': 'productRelation',
                            'type': {
                                'name': 'ProductRelation'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'CreateProductRelation'
                },
                {
                    'description': 'An input to createProductRelation()',
                    'fields': None,
                    'inputFields': [
                        {
                            'defaultValue': None,
                            'description': 'The typeId of the product relation type of the relation from "self" to the "other"',
                            'name': 'typeId'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The productId of the self product',
                            'name': 'selfProductId'
                        },
                        {
                            'defaultValue': None,
                            'description': 'The productId of the other product',
                            'name': 'otherProductId'
                        }
                    ],
                    'name': 'CreateProductRelationInput'
                },
                {
                    'description': '''Remove relations from two products.

    ''',
                    'fields': [
                        {
                            'description': None,
                            'name': 'ok',
                            'type': {
                                'name': 'Boolean'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'DeleteProductRelation'
                },
                {
                    'description': None,
                    'fields': [
                        {
                            'description': None,
                            'name': 'authPayload',
                            'type': {
                                'name': 'AuthPayload'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'GitHubAuth'
                },
                {
                    'description': None,
                    'fields': [
                        {
                            'description': None,
                            'name': 'token',
                            'type': {
                                'name': 'String'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'AuthPayload'
                },
                {
                    'description': None,
                    'fields': [
                        {
                            'description': None,
                            'name': 'ok',
                            'type': {
                                'name': 'Boolean'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': 'StoreAdminAppToken'
                },
                {
                    'description': 'A GraphQL Schema defines the capabilities of a GraphQL server. It exposes all available types and directives on the server, as well as the entry points for query, mutation and subscription operations.',
                    'fields': [
                        {
                            'description': 'A list of all types supported by this server.',
                            'name': 'types',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': 'The type that query operations will be rooted at.',
                            'name': 'queryType',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': 'If this server supports mutation, the type that mutation operations will be rooted at.',
                            'name': 'mutationType',
                            'type': {
                                'name': '__Type'
                            }
                        },
                        {
                            'description': 'If this server support subscription, the type that subscription operations will be rooted at.',
                            'name': 'subscriptionType',
                            'type': {
                                'name': '__Type'
                            }
                        },
                        {
                            'description': 'A list of all directives supported by this server.',
                            'name': 'directives',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': '__Schema'
                },
                {
                    'description': '''The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.

Depending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name and description, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.''',
                    'fields': [
                        {
                            'description': None,
                            'name': 'kind',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'name',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'description',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'fields',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'interfaces',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'possibleTypes',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'enumValues',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'inputFields',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'ofType',
                            'type': {
                                'name': '__Type'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': '__Type'
                },
                {
                    'description': 'An enum describing what kind of type a given `__Type` is',
                    'fields': None,
                    'inputFields': None,
                    'name': '__TypeKind'
                },
                {
                    'description': 'Object and Interface types are described by a list of Fields, each of which has a name, potentially a list of arguments, and a return type.',
                    'fields': [
                        {
                            'description': None,
                            'name': 'name',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'description',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'args',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'type',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'isDeprecated',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'deprecationReason',
                            'type': {
                                'name': 'String'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': '__Field'
                },
                {
                    'description': 'Arguments provided to Fields or Directives and the input fields of an InputObject are represented as Input Values which describe their type and optionally a default value.',
                    'fields': [
                        {
                            'description': None,
                            'name': 'name',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'description',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'type',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'defaultValue',
                            'type': {
                                'name': 'String'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': '__InputValue'
                },
                {
                    'description': 'One possible value for a given Enum. Enum values are unique values, not a placeholder for a string or numeric value. However an Enum value is returned in a JSON response as a string.',
                    'fields': [
                        {
                            'description': None,
                            'name': 'name',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'description',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'isDeprecated',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'deprecationReason',
                            'type': {
                                'name': 'String'
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': '__EnumValue'
                },
                {
                    'description': '''A Directive provides a way to describe alternate runtime execution and type validation behavior in a GraphQL document.

In some cases, you need to provide options to alter GraphQL's execution behavior in ways field arguments will not suffice, such as conditionally including or skipping a field. Directives provide this by describing additional information to the executor.''',
                    'fields': [
                        {
                            'description': None,
                            'name': 'name',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'description',
                            'type': {
                                'name': 'String'
                            }
                        },
                        {
                            'description': None,
                            'name': 'locations',
                            'type': {
                                'name': None
                            }
                        },
                        {
                            'description': None,
                            'name': 'args',
                            'type': {
                                'name': None
                            }
                        }
                    ],
                    'inputFields': None,
                    'name': '__Directive'
                },
                {
                    'description': 'A Directive can be adjacent to many parts of the GraphQL language, a __DirectiveLocation describes one such possible adjacencies.',
                    'fields': None,
                    'inputFields': None,
                    'name': '__DirectiveLocation'
                }
            ]
        }
    }
}
