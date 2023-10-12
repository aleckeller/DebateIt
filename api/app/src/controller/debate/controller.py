from sqlalchemy import select, func, insert, update, case
from sqlalchemy.orm import Session, aliased

from ...service.files import FileService
from models import Debate, DebateCategory, Response, User, debate_debate_category_table
from .model import CreateDebate, UploadFile, CreateResponse, GetDebate


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
            func.count(func.distinct(Response.id)).label("responses"),
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


def create_response(session: Session, response: CreateResponse) -> int:
    """
    Creates a response
    """
    return (
        session.execute(
            insert(Response).returning(Response),
            response.bind_vars(),
        )
        .first()[0]
        .id
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
            case(
                (
                    Response.id.isnot(None),
                    func.jsonb_agg(
                        func.jsonb_build_object(
                            "id",
                            Response.id,
                            "body",
                            Response.body,
                            "agree",
                            Response.agree,
                            "disagree",
                            Response.disagree,
                            "created_by",
                            urcb_alias.username.label("created_by"),
                        ).distinct()
                    ),
                ),
                else_="[]",
            ).label("responses"),
            ucb_alias.username.label("created_by"),
            uw_alias.username.label("winner"),
        )
        .outerjoin(Response, Debate.id == Response.debate_id)
        .outerjoin(DebateCategory, Debate.debate_categories)
        .outerjoin(ucb_alias, Debate.created_by)
        .outerjoin(uw_alias, Debate.winner)
        .outerjoin(urcb_alias, Response.user)
        .group_by(
            Debate.id,
            Debate.title,
            Debate.summary,
            Debate.picture_url,
            Response.id,
            ucb_alias.username,
            uw_alias.username,
        )
        .where(Debate.id == get_debate_model.debate_id)
    )

    result = session.execute(stmt).first()

    return result._asdict() if result else {}
