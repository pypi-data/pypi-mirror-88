
##__________________________________________________________________||
FRAGMENT_PRODUCT_SHALLOW = '''
fragment fragmentProductShallow on Product {
  productId
  typeId
  name
}
'''

FRAGMENT_PRODUCT_CONNECTION_SHALLOW = '''
fragment fragmentProductConnectionShallow on ProductConnection {
  edges {
    node {
     ...fragmentProductShallow
    }
  }
}
''' + FRAGMENT_PRODUCT_SHALLOW

##__________________________________________________________________||
FRAGMENT_PRODUCT_DEEP = '''
fragment fragmentProductDeep on Product {
  productId
  typeId
  type_ {
    typeId
    name
  }
  name
  contact
  dateProduced
  producedBy
  datePosted
  postedBy
  dateUpdated
  updatedBy
  paths {
    edges {
      node {
        pathId
        path
        note
      }
    }
  }
  relations {
    edges {
      node {
        relationId
        typeId
        type_ {
          typeId
          name
        }
        otherProductId
        other {
          productId
          typeId
          type_ {
            typeId
            name
          }
          name
        }
        reverseRelationId
        reverse {
          relationId
          typeId
          type_ {
            typeId
            name
          }
        }
      }
    }
  }
  note
}
'''

FRAGMENT_PRODUCT_CONNECTION_DEEP = '''
fragment fragmentProductConnectionDeep on ProductConnection {
  edges {
    node {
     ...fragmentProductDeep
    }
  }
}
''' + FRAGMENT_PRODUCT_DEEP

##__________________________________________________________________||
CREATE_PRODUCT = '''
mutation CreateProduct($input: CreateProductInput!) {
  createProduct(input: $input) {
    ok
    product {
      ...fragmentProductDeep
    }
  }
}
''' + FRAGMENT_PRODUCT_DEEP

DELETE_PRODUCT = '''
mutation DeleteProduct($productId: Int!) {
  deleteProduct(productId: $productId) {
    ok
  }
}
'''

UPDATE_PRODUCT = '''
mutation($productId: Int!, $input: UpdateProductInput!) {
  updateProduct(productId: $productId, input: $input) {
    ok
    product {
      ...fragmentProductDeep
    }
  }
}
''' + FRAGMENT_PRODUCT_DEEP

##__________________________________________________________________||
