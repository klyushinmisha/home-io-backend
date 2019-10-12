import arrow
from flask_bcrypt import Bcrypt, \
    generate_password_hash, check_password_hash
from sqlalchemy_utils import ArrowType

from . import db
from .device import Device


class User(db.Model):
    __tablename__ = "user"

    baked_query = db.bakery(lambda session: session.query(User))

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    
    _password_hash = db.Column(db.Binary(72), nullable=False)
    password = property()

    @password.setter
    def password(self, value):
        self._password_hash = generate_password_hash(value)

    def check_password(self, value):
        check_password_hash(self._password_hash, value)

    created_at = db.Column(
        ArrowType,
        default=arrow.utcnow
    )

    devices = db.relationship(
        Device,
        backref='user',
        cascade='all, delete-orphan'
    )
