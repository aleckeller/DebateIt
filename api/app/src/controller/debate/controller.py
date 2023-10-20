from sqlalchemy import (
    select,
    func,
    insert,
    update,
    case,
    literal,
    String,
    Case,
)
from sqlalchemy.orm import Session, aliased

from ...service.files import FileService
from models import (
    Debate,
    DebateCategory,
    Response,
    User,
    debate_debate_category_table,
    Vote,
)
from .model import CreateDebate, UploadFile, GetDebate


def get_debates(session: Session) -> list[dict]:
    """
    Returns list of debates
    """
    ucb_alias = aliased(User)
    uw_alias = aliased(User)

    stmt = (
        select(
            Debate.id,
            Debate.title,
            func.array_agg(func.distinct(DebateCategory.name)).label("category_names"),
            Debate.summary,
            Debate.picture_url,
            _get_end_at(),
            func.count(func.distinct(Response.id)).label("response_count"),
            ucb_alias.username.label("created_by"),
            uw_alias.username.label("leader"),
        )
        .outerjoin(Response, Debate.id == Response.debate_id)
        .outerjoin(DebateCategory, Debate.debate_categories)
        .outerjoin(ucb_alias, Debate.created_by)
        .outerjoin(uw_alias, Debate.leader)
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


def update_file_location(upload_file: UploadFile, session: Session):
    """
    Updates db to file location
    """
    condition = Debate.id == upload_file.debate_id
    update_stmt = (
        update(Debate).where(condition).values(picture_url=upload_file.file_location)
    )
    session.execute(update_stmt)


def upload_file(file_service: FileService, upload_file: UploadFile) -> dict:
    """
    Uploads file using service
    """
    return file_service.upload(upload_file.file_bytes, upload_file.file_location)


_vote_counts_subquery = (
    select(
        Vote.response_id,
        func.sum(case((Vote.vote_type == "AGREE", 1), else_=0)).label("agree_count"),
        func.sum(case((Vote.vote_type == "DISAGREE", 1), else_=0)).label(
            "disagree_count"
        ),
    )
    .group_by(Vote.response_id)
    .alias("v")
)


def _vote_enabled_subquery(user_id: int, vote_type: str):
    return (
        select(Response.id)
        .join(Vote, Vote.response_id == Response.id)
        .filter(Vote.vote_type == vote_type)
        .filter(Vote.created_by_id == user_id)
        .distinct()
        .alias("agree_responses")
        .select()
    )


def get_debate(session: Session, get_debate_model: GetDebate) -> dict:
    """
    Get a debate
    """
    ucb_alias = aliased(User)
    uw_alias = aliased(User)
    urcb_alias = aliased(User)

    stmt = (
        select(
            Debate.id,
            Debate.title,
            func.array_agg(func.distinct(DebateCategory.name)).label("category_names"),
            Debate.summary,
            Debate.picture_url,
            _get_end_at(),
            case(
                (
                    func.count(Response.id) > 0,
                    func.jsonb_agg(
                        func.jsonb_build_object(
                            "id",
                            Response.id,
                            "body",
                            Response.body,
                            "created_by",
                            urcb_alias.username.label("created_by"),
                            "agree",
                            func.coalesce(_vote_counts_subquery.c.agree_count, 0),
                            "disagree",
                            func.coalesce(_vote_counts_subquery.c.disagree_count, 0),
                            "agreeEnabled",
                            case(
                                (
                                    Response.id.in_(
                                        _vote_enabled_subquery(1, "AGREE")
                                    ),  # TODO: Update user ID when authentication system is implemented
                                    False,
                                ),
                                else_=True,
                            ),
                            "disagreeEnabled",
                            case(
                                (
                                    Response.id.in_(
                                        _vote_enabled_subquery(1, "DISAGREE")
                                        # TODO: Update user ID when authentication system is implemented
                                    ),
                                    False,
                                ),
                                else_=True,
                            ),
                        ).distinct()
                    ),
                ),
                else_="[]",
            ).label("responses"),
            ucb_alias.username.label("created_by"),
            uw_alias.username.label("leader"),
        )
        .outerjoin(Response, Debate.id == Response.debate_id)
        .outerjoin(DebateCategory, Debate.debate_categories)
        .outerjoin(Vote, Response.id == Vote.response_id)
        .outerjoin(ucb_alias, Debate.created_by)
        .outerjoin(uw_alias, Debate.leader)
        .outerjoin(urcb_alias, Response.user)
        .outerjoin(
            _vote_counts_subquery, Response.id == _vote_counts_subquery.c.response_id
        )
        .group_by(
            Debate.id,
            Debate.title,
            Debate.summary,
            Debate.picture_url,
            ucb_alias.username,
            uw_alias.username,
        )
        .where(Debate.id == get_debate_model.debate_id)
    )

    result = session.execute(stmt).first()

    return result._asdict() if result else {}


def _get_end_at() -> Case:
    current_date = func.now()
    return case(
        (
            current_date > Debate.end_at,
            literal("Finished"),
        ),
        (
            func.extract("day", Debate.end_at - current_date) > 0,
            (
                func.extract("day", Debate.end_at - current_date).cast(String)
                + "d "
                + func.extract("hour", Debate.end_at - current_date).cast(String)
                + "h "
                + func.extract("minute", Debate.end_at - current_date).cast(String)
                + "m"
            ),
        ),
        (
            func.extract("hour", Debate.end_at - current_date) > 0,
            (
                func.extract("hour", Debate.end_at - current_date).cast(String)
                + "h "
                + func.extract("minute", Debate.end_at - current_date).cast(String)
                + "m"
            ),
        ),
        else_=(func.extract("minute", Debate.end_at - current_date).cast(String) + "m"),
    ).label("end_at")
