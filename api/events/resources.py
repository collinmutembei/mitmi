from flask_restful import Resource, fields, marshal
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.app import db
from api.events.models import Event

event_fields = {
    "id": fields.Integer,
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

    @jwt_required
    def get(self):
        all_events = Event.query.all()
        return marshal(all_events, event_fields), 200


class ViewEvent(Resource):
    """ Enables logged-in users to view specific event:
    """

    @jwt_required
    def get(self, id):

        if id:
            event = Event.query.get(id)

            if event:
                return marshal(event, event_fields), 200
            else:
                return {"message": "no such event"}, 404

    @jwt_required
    def put(self, id):
        user = get_jwt_identity()

        if id:
            event = Event.query.filter_by(id=id, created_by=user).first()

            if event:
                parser = RequestParser()
                parser.add_argument("name", type=str)
                parser.add_argument("venue", type=str)
                args = parser.parse_args()

                event.name = args.name or event.name
                event.venue = args.venue or event.venue

                db.session.add(event)
                db.session.commit()
                return marshal(event, event_fields), 200
            else:
                return {"message": "no such event"}, 404
