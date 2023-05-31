from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config.DevelopmentConfig")

    from db import init_db, connector

    app.cli.add_command(init_db)
    connector.init_app(app)

    from routes import base_router

    app.register_blueprint(base_router)

    from middleware import add_middlewares

    add_middlewares(app)

    return app
