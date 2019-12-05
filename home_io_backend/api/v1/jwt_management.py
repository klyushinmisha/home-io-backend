import uuid

from ... import app, jwt
from ...models import User, Device


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    with app.app_context():
        try:
            # NOTE: only device can have uuid
            # FIXME: bad auth schema, user can be compromised
            uuid.UUID(identity)
        except ValueError:
            return User.query.filter(
                User.username == identity
            ).one_or_none()
        device = Device.query.get(identity)
        return device.users.filter(
            User.username == identity
        ).one_or_none()
