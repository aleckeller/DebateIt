from sqlalchemy import insert
from sqlalchemy.orm import Session

from models import User
from model import CreateUser


def create_user(session: Session, create_user_model: CreateUser) -> int:
    """
    Creates a response
    """
    return (
        session.execute(
            insert(User).returning(User),
            create_user_model.bind_vars(),
        )
        .first()[0]
        .id
    )
