
##__________________________________________________________________||
FRAGMENT_PRODUCT_RELATION_TYPE = '''
fragment fragmentProductRelationType on ProductRelationType {
  typeId
  name
  indefArticle
  singular
  plural
  reverse {
    typeId
    name
  }
  relations {
    edges {
      node {
        self_ {
          productId
          name
        }
        other {
          productId
          name
        }
      }
    }
  }
}
'''

FRAGMENT_PRODUCT_RELATION_TYPE_CONNECTION = '''
fragment fragmentProductRelationTypeConnection on ProductRelationTypeConnection {
  edges {
    node {
      ...fragmentProductRelationType
    }
  }
}
''' + FRAGMENT_PRODUCT_RELATION_TYPE

##__________________________________________________________________||
CREATE_PRODUCT_RELATION_TYPES = '''
mutation CreateProductRelationTypes(
    $type: CreateProductRelationTypeInput!,
    $reverse: CreateProductRelationTypeInput,
    $selfReverse: Boolean) {
  createProductRelationTypes(type: $type, reverse: $reverse, selfReverse: $selfReverse) {
    ok
    productRelationType {
      ...fragmentProductRelationType
    }
  }
}
''' + FRAGMENT_PRODUCT_RELATION_TYPE

DELETE_PRODUCT_RELATION_TYPES = '''
mutation DeleteProductRelationTypes($typeId: Int!) {
  deleteProductRelationTypes(typeId: $typeId) {
    ok
  }
}
'''

UPDATE_PRODUCT_RELATION_TYPE = '''
mutation UpdateProductRelationType(
    $typeId: Int!, $input: UpdateProductRelationTypeInput!) {
  updateProductRelationType(typeId: $typeId, input: $input) {
    ok
    productRelationType {
      ...fragmentProductRelationType
    }
  }
}
''' + FRAGMENT_PRODUCT_RELATION_TYPE

##__________________________________________________________________||
