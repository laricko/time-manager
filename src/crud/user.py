from sqlalchemy import select
from werkzeug.exceptions import BadRequest

from db import connector
from models import User

def create_user(data: dict) -> None:
    username = data["username"]
    if get_user_by_username(username):
        raise BadRequest("Username already exists")
    user = User(username=username)
    user.set_password(data["password"])
    connector.session.add(user)
    connector.session.commit()


def get_user_by_username(username: str) -> User | None:
    query = select(User).where(User.username==username)
    user = connector.session.scalars(query).first()
    return user
