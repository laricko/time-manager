from flask import Blueprint, request
from werkzeug.exceptions import BadRequest

import crud_task
from auth import only_authenticated
from models import Task

statistic_router = Blueprint("statistic", __name__, url_prefix="statistic")


SLEEP_TIME = 28800  # Must be in user settings
ONE_DAY_SECODS_AMOUNT = 86400 - SLEEP_TIME


def collect_statistic(tasks: list[Task]) -> dict:
    # Implement logic
    return [task.as_dict() for task in tasks]
    # result = {}
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
    if "start" not in request.args or "finish" not in request.args:
        return {
            "detail": "start and finish datetimes must be in params"
        }, BadRequest.code
    start = request.args["start"]
    finish = request.args["finish"]
    user = request.environ["user"]
    tasks = crud_task.get_tasks(user, start=start, finish=finish)
    return collect_statistic(tasks)
