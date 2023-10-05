from sqlalchemy import select, text
from sqlalchemy.orm import Session

from models import Debate


def get_debates(session: Session):
    """
    Returns list of debates
    """
    debates = session.execute(select(Debate)).scalars().all()
    return [debate.to_dict() for debate in debates]
