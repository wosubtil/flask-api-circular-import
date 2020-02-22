from flask import Blueprint, request

from helpers.response import custom_response
from models.user_model import UserModel

users_resource = Blueprint('users', __name__)


@users_resource.route('/users', methods=['POST'])
def create():
    try:
        user_data = request.get_json()
        user = UserModel(user_data)
        user.save()
        return custom_response({'message': 'Usuário criado com sucesso!', 'id': user.id}, 200)
    except Exception as e:
        print(e)
        return custom_response({'message': 'Houve um erro ao criar o Usuário'}, 400)
