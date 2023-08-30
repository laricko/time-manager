from flask import Blueprint, request

from auth import only_authenticated
from crud import interest as crud


interest_router = Blueprint("interest", __name__, url_prefix="/interest")


@interest_router.get("/", endpoint="all_interests")
@only_authenticated
def all_interests():
    interests = crud.get_all_interests()
    return [interest.as_dict() for interest in interests]


@interest_router.get("/my", endpoint="user_interests")
@only_authenticated
def user_interests():
    interests = crud.get_user_interests(request.environ["user"].id)
    return [interest.as_dict() for interest in interests]


@interest_router.post("/add", endpoint="add_interest")
@only_authenticated
def add_interest():
    crud.add_interest_to_user(request.form["interest_id"], request.form["user_id"])
    return {"detail": "success"}


@interest_router.delete("/delete", endpoint="delete_interest")
@only_authenticated
def delete_interest():
    crud.delete_interest_from_user(request.form["interest_id"], request.form["user_id"])
    return {"detail": "success"}
