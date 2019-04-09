from flask_restful import Resource, fields, marshal
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import create_access_token

from ..app import db
from ..users.models import User

user_fields = {
    'username': fields.String,
}


class SignUp(Resource):
    """creates a user:
            POST {"username": "patientzer0", "password": "YmlnZ2VzdGJlaGluZA"}
    """
    def post(self):

        parser = RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        signup_user = User.query.filter_by(username=args.username).first()
        if signup_user:
            return {'message': 'user with that name already exists'}, 400

        signup_user = User(
            username=args.username,
            password=args.password
        )
        db.session.add(signup_user)
        db.session.commit()
        return marshal(signup_user, user_fields), 201


class SignIn(Resource):
    """creates a user:
            POST {"username": "patientzer0", "password": "YmlnZ2VzdGJlaGluZA"}
    """
    def post(self):

        parser = RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        signin_user = User.query.filter_by(username=args.username).first()
        # if user exists
        if signin_user:
            # check password
            if signin_user.verify_password(args.password):
                user_token = create_access_token(identity=signin_user.id)
                return {'token': user_token}, 200
            # password not correct
            return {'message': 'password did not work'}, 403
        return {'message': 'invalid user'}, 401
