import os

import openai


class Config:
    TESTING = False
    SECRET_KEY = "ixnXVzGMt7OKGnYUSHBB3sY4viSuhkZ8"
    ALGORITHM = "HS256"

    OPENAI_APIKEY = "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"
    openai.api_key = OPENAI_APIKEY

    os.environ["SECRET_KEY"] = SECRET_KEY
    os.environ["ALGORITHM"] = ALGORITHM

    JWT_EXPIRE_MINUTES = "60"

    _POSTGRES_DB = "postgres"
    _POSTGRES_USER = "postgres"
    _POSTGRES_PASSWORD = "postgres"
    _POSTGRES_HOST = "db"

    @property
    def DATABASE_URI(self):
        uri = f"postgresql://{self._POSTGRES_USER}:{self._POSTGRES_PASSWORD}@{self._POSTGRES_HOST}:5432/{self._POSTGRES_DB}"
        return uri


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEVELOPMENT = True


class TestingConfig(Config):
    TESTING = True
    DEVELOPMENT = False
    _POSTGRES_HOST = "0.0.0.0"
    _POSTGRES_DB = "postgres_test"
