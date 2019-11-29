from ... import app, jwt
from ...models import User


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    with app.app_context():
        return User.query.filter(
            User.username == identity
        ).one_or_none()
