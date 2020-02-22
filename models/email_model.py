
from . import db
from sqlalchemy import func
from marshmallow import fields, Schema

from .user_model import UserModel, UserSchema


class EmailModel(db.Model):

    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    sender = db.Column(db.String(200), nullable=False)
    id_users = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('UserModel')


    def save(self):
        db.session.add(self)
        db.session.commit()


    @staticmethod
    def get_all(page, size):
        email_schema = EmailSchema()
        email_model = EmailModel.query \
                                .join(UserModel, UserModel.id == EmailModel.id_users)
        
        email_model = email_model.paginate(page=page,
                                           per_page=size,
                                           error_out=False)

        email_serialized = email_schema.dump(email_model.items, many=True)
        EmailModel.get_total_by_user(2)
        return dict(items=email_serialized, total=email_model.total)


    @staticmethod
    def get_total_by_user(id_user):
        q = EmailModel.query.filter_by(id_users=id_user)
        return q.count()



class EmailSchema(Schema):

    id = fields.Int(dump_only=True)
    subject = fields.Str(required=True)
    content = fields.Str(required=True)
    sender = fields.Str(require=True)
    id_users = fields.Int(required=True)
    user = fields.Nested(UserSchema)