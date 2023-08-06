from ..db.sa import sa

##__________________________________________________________________||
class Product(sa.Model):
    __tablename__ = 'products'
    product_id = sa.Column(sa.Integer(), primary_key=True)
    type_id = sa.Column(
        sa.ForeignKey('product_types.type_id'),
        nullable=False
    )
    type_ = sa.relationship("ProductType", backref=sa.backref("products"))
    name = sa.Column(sa.Text(), nullable=False)
    contact = sa.Column(sa.Text())
    date_produced = sa.Column(sa.Date())
    produced_by = sa.Column(sa.Text())
    date_posted = sa.Column(sa.Date())
    posted_by = sa.Column(sa.Text())
    date_updated = sa.Column(sa.Date())
    updated_by = sa.Column(sa.Text())
    note = sa.Column(sa.Text())
    __table_args__ = (sa.UniqueConstraint('type_id', 'name', name='_type_id_name'), )

##__________________________________________________________________||
