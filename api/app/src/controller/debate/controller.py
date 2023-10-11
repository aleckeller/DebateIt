from sqlalchemy import select, func, insert
from sqlalchemy.orm import Session, aliased

from models import Debate, DebateCategory, Response, User
from .model import CreateDebate


def get_debates(session: Session):
    """
    Returns list of debates
    """
    ucb_alias = aliased(User)
    uw_alias = aliased(User)

    stmt = (
        select(
            Debate.id,
            Debate.title,
            DebateCategory.name.label("category_name"),
            Debate.summary,
            Debate.picture_url,
            func.count(Response.id).label("responses"),
            ucb_alias.username.label("created_by"),
            uw_alias.username.label("winner"),
        )
        .outerjoin(Response, Debate.id == Response.debate_id)
        .outerjoin(DebateCategory, Debate.debate_categories)
        .outerjoin(ucb_alias, Debate.created_by)
        .outerjoin(uw_alias, Debate.winner)
        .group_by(
            Debate.id,
            Debate.title,
            DebateCategory.name,
            Debate.summary,
            Debate.picture_url,
            ucb_alias.username,
            uw_alias.username,
        )
        .order_by(Debate.created_at.desc())
    )

    results = session.execute(stmt)
    return [row._asdict() for row in results]


def create_debate(session: Session, debate: CreateDebate) -> int:
    """
    Creates a debate
    """
    return (
        session.execute(
            insert(Debate).returning(Debate),
            debate.bind_vars(),
        )
        .first()[0]
        .id
    )
