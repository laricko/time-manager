from typing import Literal
from datetime import datetime

from sqlalchemy import select, and_, Select

from db import connector
from models import User, Task


TypeChoices = Literal["past", "present", "future"]


def get_query_to_get_tasks_depends_on_type(
    user_id: int, type: TypeChoices | None
) -> Select:
    query = select(Task).where(Task.user_id == user_id)
    now = datetime.now()
    if type == "past":
        query = query.where(Task.finish < now)
    elif type == "present":
        query = query.where(and_(Task.start < now, Task.finish > now))
    elif type == "future":
        query = query.where(Task.start > now)
    return query


def get_tasks(user: User, type: TypeChoices | None) -> list[dict]:
    query = get_query_to_get_tasks_depends_on_type(user.id, type)
    tasks = connector.session.scalars(query).all()
    result = [task.as_dict() for task in tasks]
    return result


def create_task(user: User, data: dict) -> None:
    task = Task(
        user_id=user.id,
        title=data["title"],
        description=data["description"],
        start=data["start"],
        finish=data["finish"],
    )
    connector.session.add(task)
    connector.session.commit()
