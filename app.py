from flask import Flask

from config import app_config
from models import db

from helpers.response import custom_response

from resources.user import users_resource
from resources.email import email_resource


def create_app(env_name):
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(users_resource, url_prefix='/api/')
    app.register_blueprint(email_resource, url_prefix='/api/')

    @app.errorhandler(404)
    def route_not_found(e):
        return custom_response({'erro': 'Recurso não encontrado'}, 404)

    return app
