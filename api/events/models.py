from api.app import db
from api.users.models import User

guests = db.Table(
    'guests',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)


class Event(db.Model):
    """ Model defining user
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    venue = db.Column(db.String(80))
    max_guests = db.Column(db.String(80))
    guest = db.relationship(
        'User',
        secondary=guests,
        backref=db.backref('event', lazy='dynamic')
    )

    def is_full(self, plaintext):
        """Returns true if event has reached max capacity of guests
        """
        pass

    def remaining_slots(self, plaintext):
        """Returns number of remaining guest slots till event is full
        """
        pass

    def __repr__(self):
        return '<Event {0} happening at {1} : {2} Slots remaining>'.format(
            self.name,
            self.venue,
            self.remaining
        )
