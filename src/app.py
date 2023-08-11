from flask import Flask
from flask_cors import CORS


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.config.from_object("config.DevelopmentConfig")

    from db import connector, init_db

    app.cli.add_command(init_db)
    connector.init_app(app)

    from routes import base_router

    app.register_blueprint(base_router)

    from middleware import add_middlewares

    add_middlewares(app)

    return app
