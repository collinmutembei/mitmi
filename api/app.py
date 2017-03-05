import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_jwt_extended import JWTManager

from api.config import config


app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

# import in the middle of code to avoid cyclic imports
from api.users.models import User

# Set the config for app
config_name = os.environ.get('APP_SETTINGS', 'default')
app.config.from_object(config[config_name])

# import in the middle of code to avoid cyclic imports
from api.users.resources import SignUp, SignIn
from api.events.resources import CreateEvent, ViewEvent

api.add_resource(SignUp, '/signup/')
api.add_resource(SignIn, '/signin/')

api.add_resource(CreateEvent, '/event/')
api.add_resource(ViewEvent, '/event/<int:id>/')
