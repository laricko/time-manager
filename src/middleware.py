from flask import Flask
from werkzeug.wrappers import Request

from auth import get_user


class AuthMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        environ["user"] = get_user(request)
        return self.app(environ, start_response)


def add_middlewares(app: Flask):
    app.wsgi_app = AuthMiddleware(app.wsgi_app)
