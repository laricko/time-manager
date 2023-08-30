from flask import request
from sqlalchemy import select
from werkzeug.exceptions import Forbidden
from werkzeug.wrappers import Request

from db import connector
from security import decode_access_token
from models import User


def only_authenticated(view: callable):
    def check_user(*args, **kwargs):
        user = request.environ["user"]
        if not user.is_authenticated:
            raise Forbidden
        return view(*args, **kwargs)

    return check_user


class AnonymousUser:
    id = None
    is_anonymous = True
    is_authenticated = False

    def __repr__(self) -> str:
        return "Anonymous User"


anonymous_user = AnonymousUser()


def get_user(request: Request):
    creds = request.authorization
    if not creds:
        return anonymous_user
    _, token = creds.to_header().split(" ")
    decoded = decode_access_token(token)
    if not decoded:
        return anonymous_user
    return _get_user(decoded["sub"])


def _get_user(username: str) -> User:
    query = select(User).where(User.username == username)
    user = connector.session.scalars(query).first()
    return user or anonymous_user
