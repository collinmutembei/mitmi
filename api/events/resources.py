from flask_restful import Resource, fields, marshal
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.app import db
from api.events.models import Event

event_fields = {
    "name": fields.String,
    "venue": fields.String,
    "created_by": fields.String
}


class CreateEvent(Resource):
    """ Enables logged-in users to create event:
            POST {"name": "dunda", "venue": "B Club"}
    """

    @jwt_required
    def post(self):

        parser = RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("venue", type=str, required=True)
        args = parser.parse_args()

        user = get_jwt_identity()

        event = Event(
            name=args.name,
            venue=args.venue,
            created_by=user
        )
        db.session.add(event)
        db.session.commit()
        return marshal(event, event_fields), 201
