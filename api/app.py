import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from api.config import config


app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# Set the config for app
config_name = os.environ.get('APP_SETTINGS', 'default')
app.config.from_object(config[config_name])

# import in the middle of code to avoid cyclic imports
from api.users.models import User
