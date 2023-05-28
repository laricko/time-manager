from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config.DevelopmentConfig")

    from db import init_db, db_session

    app.cli.add_command(init_db)

    @app.teardown_request
    def close_db(e=None):
        db_session.remove()

    from routes import base_router

    app.register_blueprint(base_router)

    from middleware import add_middlewares

    add_middlewares(app)

    return app
