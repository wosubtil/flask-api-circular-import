from flask import Blueprint, request

from models.email_model import EmailModel
from helpers.response import custom_response

email_resource = Blueprint('emails', __name__)


@email_resource.route('/emails', methods=['POST'])
def create():
    try:
        email_data = request.get_json()
        email = EmailModel(email_data)
        email.save()
        return custom_response({'message': 'Email criado com sucesso!', 'id': email.id}, 200)
    except Exception as e:
        print(e)
        return custom_response({'message': 'Houve um erro ao criar o Email'}, 400)


@email_resource.route('/emails', methods=['GET'])
def get_all():
    page = int(request.args.get('page'))
    size = int(request.args.get('size'))

    emails = EmailModel.get_all(page, size)
    items = emails.get('items')
    total = emails.get('total')
    return custom_response(dict(data=items, meta=dict(total=total)), 200)

