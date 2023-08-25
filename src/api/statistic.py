from datetime import timedelta, datetime

from flask import Blueprint, request
from werkzeug.exceptions import BadRequest

from crud import task as crud
from auth import only_authenticated
from models import Task

statistic_router = Blueprint("statistic", __name__, url_prefix="statistic")


SLEEP_TIME = 28800  # Must be in user settings


def collect_statistic(tasks: list[Task], start: datetime, finish: datetime) -> dict:
    result = {}

    result["task_qty"] = len(tasks)

    sum_task_duration = timedelta()
    for task in tasks:
        sum_task_duration += task.duration
    result["sum_task_duration"] = str(sum_task_duration)

    period: timedelta = finish - start
    result["period"] = str(period)
    sleep_time_in_period = period.days * SLEEP_TIME
    work_time_in_period = period.total_seconds() - sleep_time_in_period
    result["free_time_percentale"] = int(
        sum_task_duration.total_seconds() * 100 / work_time_in_period
    )
    result["sleep_time"] = str(timedelta(seconds=sleep_time_in_period))

    return result


@statistic_router.get("/", endpoint="get_statistic")
@only_authenticated
def statistic():
    if "start" not in request.args or "finish" not in request.args:
        return {
            "detail": "start and finish datetimes must be in params"
        }, BadRequest.code
    start = request.args["start"]
    finish = request.args["finish"]
    start = datetime.fromisoformat(start)
    finish = datetime.fromisoformat(finish)
    user = request.environ["user"]
    tasks = crud.get_tasks(user, start=start, finish=finish)
    return collect_statistic(tasks, start, finish)
