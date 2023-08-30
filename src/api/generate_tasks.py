from flask import Blueprint, request
import openai

from auth import only_authenticated
from crud.task import get_tasks_for_user

task_generation_router = Blueprint(
    "task_generation", __name__, url_prefix="/task-generate"
)


ENGINE = "text-davinci-003"
TOKENS = 150


@task_generation_router.post("/")
@only_authenticated
def generate_tasks():
    return "need chatgpt"
    # user = request.environ["user"]
    # tasks = get_tasks_for_user(user)
    # tasks_jsonable = [task.as_dict() for task in tasks]
    # prompt = f"Generate same schemas schedule for based on this tasks. {tasks_jsonable}"
    # openai_response = openai.Completion.create(
    #     engine=ENGINE, prompt=prompt, temperature=0.6
    # )
    # generated_schedule = openai_response.choices[0].text
    # return openai_response.choices
