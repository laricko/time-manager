import click
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


db_url = os.environ.get("DATABASE_URI")
engine = create_engine(db_url)
session_factory = sessionmaker(engine)
db_session = scoped_session(session_factory)


@click.command("init-db")
def init_db():
    """Clear the existing data and create new tables."""

    from models import Base

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    click.echo("Initialized the database.")
