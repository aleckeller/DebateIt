from sqlalchemy import select, func, insert
from sqlalchemy.orm import Session, aliased

from models import Debate, DebateCategory, Response, User, debate_debate_category_table
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
            func.array_agg(DebateCategory.name).label("category_names"),
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
    debate_id = (
        session.execute(
            insert(Debate).returning(Debate),
            debate.bind_vars(),
        )
        .first()[0]
        .id
    )
    _create_debate_debate_category_relationship(session, debate_id, debate.category_ids)
    return debate_id


def _create_debate_debate_category_relationship(
    session: Session, debate_id: id, debate_categories: list[int]
):
    session.execute(
        insert(debate_debate_category_table),
        [
            {"debate_id": debate_id, "debate_category_id": category_id}
            for category_id in debate_categories
        ],
    )
