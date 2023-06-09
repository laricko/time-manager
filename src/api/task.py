from flask import Blueprint, request

from auth import only_authenticated
import crud_task as crud

task_router = Blueprint("task", __name__, url_prefix="/task")


@task_router.get("/", endpoint="get_all_tasks")
@only_authenticated
def tasks():
    user = request.environ["user"]
    type = request.args.get("type")
    return crud.get_tasks(user, type)


@task_router.post("/", endpoint="create_task")
@only_authenticated
def create_task():
    user = request.environ["user"]
    data = request.form
    crud.create_task(user, data)
    return data
