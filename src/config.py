import os


class Config:
    TESTING = False


class ProductionConfig(Config):
    DATABASE_URI = "mysql://user@localhost/foo"


class DevelopmentConfig(Config):
    DATABASE = "db.sqlite3"
    DEVELOPMENT = True

    _POSTGRES_DB = "postgres"
    _POSTGRES_USER = "postgres"
    _POSTGRES_PASSWORD = "postgres"

    DATABASE_URI = f"postgresql://{_POSTGRES_USER}:{_POSTGRES_PASSWORD}@0.0.0.0:5432/{_POSTGRES_DB}"
    os.environ["DATABASE_URI"] = DATABASE_URI


class TestingConfig(Config):
    DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
