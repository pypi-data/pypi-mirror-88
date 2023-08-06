from ..db.sa import sa

##__________________________________________________________________||
class ProductFilePath(sa.Model):
    __tablename__ = 'product_file_paths'
    path_id = sa.Column(sa.Integer(), primary_key=True)
    path = sa.Column(sa.Text())
    note = sa.Column(sa.Text())
    product_id = sa.Column(sa.ForeignKey('products.product_id'))
    product = sa.relationship(
        "Product",
        backref=sa.backref("paths", cascade="all, delete-orphan"))

##__________________________________________________________________||
