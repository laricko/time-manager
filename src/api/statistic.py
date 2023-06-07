from datetime import timedelta, datetime

from flask import Blueprint, request
from sqlalchemy import select

from auth import only_authenticated
from db import connector
from models import Task


statistic_router = Blueprint("statistic", __name__, url_prefix="statistic")


SLEEP_TIME = 28800  # Must be in user settings
ONE_DAY_SECODS_AMOUNT = 86400 - SLEEP_TIME


def collect_statistic(tasks: list[Task]) -> dict:
    result = {}
    # Implement logic
    return result
    # sum_duration = timedelta()
    # how_much_today = 0
    # today = datetime.now().date()

    # for task in tasks:
    #     sum_duration += task.duration
    #     if task.created_at.date() == today:
    #         how_much_today += 1

    # result["sum_duration"] = str(sum_duration)
    # result["all_tasks"] = len(tasks)
    # result["how_much_today"] = how_much_today
    # result["free_time_percentale"] = int(
    #     sum_duration.seconds * 100 / ONE_DAY_SECODS_AMOUNT
    # )
    # result["free_time_value_in_seconds"] = ONE_DAY_SECODS_AMOUNT - sum_duration.seconds
    # return result


@statistic_router.get("/", endpoint="get_statistic")
@only_authenticated
def statistic():
    user = request.environ["user"]
    query = select(Task).where(Task.user_id == user.id)
    tasks = connector.session.scalars(query).all()
    return collect_statistic(tasks)
