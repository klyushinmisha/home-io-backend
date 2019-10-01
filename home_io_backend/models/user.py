from flask_bcrypt import Bcrypt

from . import db


class User(db.Model, DateMixin):
    __tablename__ = "user"

    baked_query = db.bakery(lambda session: session.query(User))

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    
    _password_hash = db.Column(db.Binary(72), nullable=False)
    password = property()

    @password.setter
    def password(value):
        self._password_hash = generate_password_hash(value)

    def check_password(value):
        check_password_hash(self._password_hash, value)
