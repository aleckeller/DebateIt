from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models import User
from model import CreateUser


def create_user(session: Session, create_user_model: CreateUser) -> int:
    """
    Creates a response
    """
    user_attributes = create_user_model.bind_vars()
    stmt = insert(User).values(user_attributes).returning(User)
    stmt = stmt.on_conflict_do_update(
        constraint="user_pkey",
        set_={col: getattr(stmt.excluded, col) for col in user_attributes},
    )
    session.execute(stmt)
