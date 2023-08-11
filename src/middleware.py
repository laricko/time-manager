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


class CorsMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def new_start_response(status: str, headers: list[tuple]):
            # NOTE: In a future this should be handeled properly
            headers.append(("Access-Control-Allow-Origin", "http://localhost:3000"))
            headers.append(("Access-Control-Allow-Headers", "*"))
            headers.append(("Access-Control-Allow-Methods", "POST,GET,OPTIONS,DELETE,PATCH"))
            headers.append(("Access-Control-Max-Age", "86400"))
            headers.append(("Access-Control-Allow-Credentials", "true"))

            return start_response(status, headers)

        return self.app(environ, new_start_response)


def add_middlewares(app: Flask):
    app.wsgi_app = CorsMiddleware(app.wsgi_app)
    app.wsgi_app = AuthMiddleware(app.wsgi_app)
