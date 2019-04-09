from ..app import db
from ..users.models import User

guests = db.Table(
    'guests',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)


class Event(db.Model):
    """ Model defining user
    """
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(
        'created_by',
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )
    name = db.Column(db.String(80), unique=True)
    venue = db.Column(db.String(80))
    guest = db.relationship(
        'User',
        secondary=guests,
        backref=db.backref('event', lazy='dynamic')
    )

    def __repr__(self):
        return '<Event {0} happening at {1}>'.format(
            self.name,
            self.venue
        )
