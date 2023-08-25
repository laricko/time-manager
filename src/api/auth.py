from flask import Blueprint, request
from werkzeug.exceptions import BadRequest

from crud import user as crud
from security import create_access_token_for_user

bad_credentials_text_error = "User with such username and password does not exist"
auth_router = Blueprint("auth", __name__, url_prefix="/auth")


@auth_router.post("/register")
def register():
    data = request.form
    crud.create_user(data)
    return data


@auth_router.post("/login")
def login():
    user = crud.get_user_by_username(request.form["username"])
    if not user:
        raise BadRequest(bad_credentials_text_error)
    password_is_correct = user.check_password(request.form["password"])
    if not password_is_correct:
        raise BadRequest(bad_credentials_text_error)
    token = create_access_token_for_user(user.username)
    result = user.as_dict()
    result["token"] = f"Bearer {token}"
    return result
