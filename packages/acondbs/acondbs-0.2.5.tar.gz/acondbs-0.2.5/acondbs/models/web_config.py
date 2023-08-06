from ..db.sa import sa

##__________________________________________________________________||
class WebConfig(sa.Model):
    __tablename__ = 'web_config'
    config_id = sa.Column(sa.Integer(), primary_key=True)
    head_title = sa.Column(sa.Text())
    toolbar_title = sa.Column(sa.Text())
    devtool_loadingstate = sa.Column(sa.Boolean())
    product_creation_dialog = sa.Column(sa.Boolean())
    product_update_dialog = sa.Column(sa.Boolean())
    product_deletion_dialog = sa.Column(sa.Boolean())

##__________________________________________________________________||
