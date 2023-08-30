from datetime import datetime, timedelta
import os

from flask import current_app
from jose.exceptions import JWTError
from jose import jwt


def create_access_token_for_user(username: str) -> str:
    to_encode = {"sub": username}
    to_encode.update(
        {
            "exp": datetime.utcnow()
            + timedelta(minutes=int(current_app.config["JWT_EXPIRE_MINUTES"]))
        }
    )
    token = jwt.encode(
        to_encode, current_app.config["SECRET_KEY"], current_app.config["ALGORITHM"]
    )
    return token


def decode_access_token(token: str):
    try:
        return jwt.decode(token, os.environ["SECRET_KEY"], os.environ["ALGORITHM"])
    except JWTError:
        return None


def check_user_admin(user, password) -> True:
    if user.username == "lari" and user.password == "string" and password == "string":
        return True
