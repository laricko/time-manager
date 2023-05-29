from base64 import b64encode

import pytest

from app import create_app
from db import init_db, db_session as session
from models import User


@pytest.fixture()
def app():
    app = create_app()
    app.config.from_object("config.TestingConfig")

    runner = app.test_cli_runner()
    runner.invoke(init_db)

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db_session():
    return session

@pytest.fixture
def test_user(db_session) -> User:
    u = User(username="username", password="password")
    db_session.add(u)
    db_session.commit()
    return db_session.get(User, 1)

@pytest.fixture
def test_user_creds(test_user) -> dict:
    to_encode = f"{test_user.username}:{test_user.password}"
    encoded = b64encode(to_encode.encode()).decode()
    return {"Authorization": f"Basic {encoded}"}

