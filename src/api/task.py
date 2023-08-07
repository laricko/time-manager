from flask import Blueprint, request

import crud_task as crud
from auth import only_authenticated

task_router = Blueprint("task", __name__, url_prefix="/task")


@task_router.get("/", endpoint="get_all_tasks")
@only_authenticated
def tasks():
    user = request.environ["user"]
    type = request.args.get("type")
    tasks = crud.get_tasks(user, type=type)
    return [task.as_dict() for task in tasks]


@task_router.post("/", endpoint="create_task")
@only_authenticated
def create_task():
    user = request.environ["user"]
    data = request.form
    crud.create_task(user, data)
    return data


@task_router.delete("/<id>", endpoint="delete_task")
@only_authenticated
def delete_task(id):
    crud.delete_task(id)
    return {"detail": "success"}


@task_router.patch("/<id>", endpoint="patch_task")
@only_authenticated
def patch_task(id):
    task = crud.patch_task(id, request.form)
    return task.as_dict()
