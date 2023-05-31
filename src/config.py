import os

_POSTGRES_DB = "postgres"
_POSTGRES_USER = "postgres"
_POSTGRES_PASSWORD = "postgres"
DATABASE_URI = (
    f"postgresql://{_POSTGRES_USER}:{_POSTGRES_PASSWORD}@0.0.0.0:5432/{_POSTGRES_DB}"
)


class Config:
    TESTING = False
    SECRET_KEY = "super_secret"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DATABASE_URI = DATABASE_URI
    os.environ["DATABASE_URI"] = DATABASE_URI


class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = f"{DATABASE_URI}_test"
    os.environ["DATABASE_URI"] = DATABASE_URI
    DEVELOPMENT = False
