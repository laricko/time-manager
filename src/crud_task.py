from datetime import datetime
from typing import Literal

from sqlalchemy import Select, and_, select

from db import connector
from models import Task, User

TypeChoices = Literal["past", "present", "future"]


def get_tasks(
    user: User,
    *,
    type: TypeChoices | None = None,
    start: datetime | None = None,
    finish: datetime | None = None,
) -> list[Task]:
    query = _get_query_to_get_tasks(user.id, type=type, start=start, finish=finish)
    return connector.session.scalars(query).all()


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


_base_query = lambda user_id: select(Task).where(Task.user_id == user_id)


def _get_query_to_get_tasks(
    user_id: int,
    *,
    type: TypeChoices | None = None,
    start: datetime | None = None,
    finish: datetime | None = None,
) -> Select:
    if type is not None:
        return _get_query_to_get_tasks_depends_on_type(user_id, type)
    if start is not None and finish is not None:
        return _get_query_to_get_tasks_depends_on_period(user_id, start, finish)
    return _base_query(user_id)


def _get_query_to_get_tasks_depends_on_period(
    user_id: int, start: datetime, finish: datetime
) -> Select:
    return _base_query(user_id).where(and_(Task.start > start, Task.finish < finish))


def _get_query_to_get_tasks_depends_on_type(user_id: int, type: TypeChoices) -> Select:
    query = _base_query(user_id)
    now = datetime.now()
    if type == "past":
        query = query.where(Task.finish < now)
    elif type == "present":
        query = query.where(and_(Task.start < now, Task.finish > now))
    elif type == "future":
        query = query.where(Task.start > now)
    return query
