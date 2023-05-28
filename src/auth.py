from base64 import b64decode

from flask import request
from sqlalchemy import select
from werkzeug.exceptions import Forbidden
from werkzeug.wrappers import Request

from db import db_session
from models import User


def only_authenticated(view: callable):
    def check_user():
        user = request.environ["user"]
        if not user.is_authenticated:
            raise Forbidden
        return view()

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
    _, token = request.authorization.to_header().split(" ")
    decoded = b64decode(token).decode()
    username, password = decoded.split(":")
    return _get_user(username, password)


def _get_user(username: str, password: str):
    query = select(User).where(User.username == username, User.password == password)
    cur = db_session.execute(query)
    if row := cur.first():
        return row._asdict().get("User")
    return anonymous_user
