from api.app import db, bcrypt


class User(db.Model):
    """ Model defining user
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(128))
    authenticated = db.Column(db.Boolean, default=False)

    def set_password(self, plaintext):
        """Hashes a password from plaintext to ciphertext
        """
        self.password = bcrypt.generate_password_hash(plaintext)

    def verify_password(self, plaintext):
        """Checks the entered paintext against the hashed password
        """
        return bcrypt.check_password_hash(self.password, plaintext)

    def __repr__(self):
        return '<User {0}>'.format(self.username)
