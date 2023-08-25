from flask import Blueprint

from api.statistic import statistic_router
from api.task import task_router
from api.auth import auth_router

base_router = Blueprint("api", __name__, url_prefix="/api")
base_router.register_blueprint(task_router)
base_router.register_blueprint(statistic_router)
base_router.register_blueprint(auth_router)
