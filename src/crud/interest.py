from sqlalchemy import select, delete, insert

from models import Interest, users_interests
from db import connector


def get_all_interests() -> list[Interest]:
    return connector.session.query(Interest).all()


def get_user_interests(user_id: int) -> list[Interest]:
    subquery = (
        select(users_interests.c.interest_id)
        .filter(users_interests.c.user_id == user_id)
        .subquery()
    )
    return connector.session.query(Interest).filter(Interest.id.in_(subquery))


def add_interest_to_user(interest_id: int, user_id: int) -> None:
    query = insert(users_interests).values(interest_id=interest_id, user_id=user_id)
    connector.session.execute(query)
    connector.session.commit()


def delete_interest_from_user(interest_id: int, user_id: int) -> None:
    query = delete(users_interests).where(
        users_interests.c.interest_id == interest_id,
        users_interests.c.user_id == user_id,
    )
    connector.session.execute(query)
    connector.session.commit()
