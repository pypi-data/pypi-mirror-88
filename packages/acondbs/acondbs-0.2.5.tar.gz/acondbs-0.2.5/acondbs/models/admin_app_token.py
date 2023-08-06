from flask import current_app
from sqlalchemy_utils import EncryptedType

from ..db.sa import sa

def encription_key():
    return current_app.config['SECRET_KEY']

##__________________________________________________________________||
class AdminAppToken(sa.Model):
    __tablename__ = 'admin_app_token'
    token_id = sa.Column(sa.Integer(), primary_key=True)
    token = sa.Column(EncryptedType(sa.Text(), key=encription_key))

##__________________________________________________________________||
