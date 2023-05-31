import click
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


@click.command("init-db")
def init_db():
    """Clear the existing data and create new tables."""

    from models import Base

    Base.metadata.drop_all(connector.engine)
    Base.metadata.create_all(connector.engine)

    click.echo("Initialized the database.")


class DatabaseConnector:
    def init_app(self, app: Flask) -> None:
        app.teardown_appcontext(self._teardown_session)

        self.engine = create_engine(app.config["DATABASE_URI"], pool_pre_ping=True)
        session_factory = sessionmaker(self.engine)
        self.session = scoped_session(session_factory)

    def _teardown_session(self, exc: BaseException | None) -> None:
        self.session.remove()


connector = DatabaseConnector()
