import os
import click

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import DATABASE_URI

db_url = os.environ.get("DATABASE_URI", f"{DATABASE_URI}_test")
engine = create_engine(db_url, pool_pre_ping=True)
session_factory = sessionmaker(engine)
db_session = scoped_session(session_factory)


@click.command("init-db")
def init_db():
    """Clear the existing data and create new tables."""

    from models import Base

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    click.echo("Initialized the database.")
