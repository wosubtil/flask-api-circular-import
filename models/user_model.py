from . import db
from marshmallow import fields, Schema

# 

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)

    
    def __init__(self, user_data):
        user_schema = UserSchema()
        user_serialized = user_schema(user_data)

        self.name = user_serialized.get('name')
        self.email = user_serialized.get('email')

    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        # Fix circular import
        from .email_model import EmailModel
        if EmailModel.get_total_by_user() == 0:
            db.session.delete(self)
            db.session.commit()
        raise Exception

    
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
