from flask import Blueprint

from auth import only_authenticated

task_router = Blueprint("task", __name__, url_prefix="/task")


@task_router.get("/")
@only_authenticated
def tasks():
    return {"hello": "world"}
