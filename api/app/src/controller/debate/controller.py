from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Debate


def get_debates(session: Session):
    """
    Returns list of debates
    """
    result = session.execute(select(Debate)).scalars().all()

    print(result)
    return result
