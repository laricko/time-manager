from flask import Blueprint, request
from sqlalchemy import select

from auth import only_authenticated
from models import Task
from db import connector

task_router = Blueprint("task", __name__, url_prefix="/task")


@task_router.get("/", endpoint="get_all_tasks")
@only_authenticated
def tasks():
    user = request.environ["user"]
    query = select(Task).where(Task.user_id == user.id)
    tasks = connector.session.scalars(query).all()
    result = [task.as_dict() for task in tasks]
    return result


@task_router.post("/", endpoint="create_task")
@only_authenticated
def create_task():
    user = request.environ["user"]
    data = request.form
    task = Task(
        user_id=user.id,
        title=data["title"],
        description=data["description"],
        finish=data["finish"],
    )
    connector.session.add(task)
    connector.session.commit()
    return data
