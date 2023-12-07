from sqlalchemy import (
    select,
    func,
    insert,
    update,
    case,
    literal,
)
from sqlalchemy.orm import Session, aliased

from ...service.files import FileService
from models import (
    Debate,
    DebateCategory,
    debate_debate_category_table,
    Vote,
    DebatesView,
    ResponsesView,
)
from .model import CreateDebate, UploadFile, GetDebate


def get_debates(session: Session) -> list[dict]:
    """
    Returns list of debates
    """
    debates = session.query(DebatesView).order_by(DebatesView.end_at).all()
    return [debate.to_dict() for debate in debates]


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


def get_debate(session: Session, get_debate_model: GetDebate) -> dict:
    """
    Get a debate
    """
    VoteAgree = aliased(Vote)
    VoteDisagree = aliased(Vote)

    query = (
        session.query(
            DebatesView.id,
            DebatesView.title,
            DebatesView.category_names,
            DebatesView.summary,
            DebatesView.picture_url,
            DebatesView.end_at,
            DebatesView.created_by,
            DebatesView.leader,
            DebatesView.response_count,
            func.to_char(DebatesView.created_at, "MM-DD-YYYY").label("created_at"),
            case(
                (func.count(ResponsesView.id) == 0, "[]"),
                else_=(
                    func.jsonb_agg(
                        func.jsonb_build_object(
                            "id",
                            ResponsesView.id,
                            "body",
                            ResponsesView.body,
                            "created_by",
                            ResponsesView.created_by,
                            "agree",
                            ResponsesView.agree,
                            "disagree",
                            ResponsesView.disagree,
                            "agree_enabled",
                            VoteAgree.id.is_(None),
                            "disagree_enabled",
                            VoteDisagree.id.is_(None),
                        )
                    )
                ),
            ).label("responses"),
        )
        .outerjoin(ResponsesView, DebatesView.id == ResponsesView.debate_id)
        .outerjoin(
            VoteAgree,
            (ResponsesView.id == VoteAgree.response_id)
            & (VoteAgree.vote_type == "agree")
            & (VoteAgree.created_by_id == get_debate_model.user_id),
        )
        .outerjoin(
            VoteDisagree,
            (ResponsesView.id == VoteDisagree.response_id)
            & (VoteDisagree.vote_type == "disagree")
            & (VoteDisagree.created_by_id == get_debate_model.user_id),
        )
        .filter(DebatesView.id == get_debate_model.debate_id)
        .group_by(
            DebatesView.id,
            DebatesView.title,
            DebatesView.category_names,
            DebatesView.summary,
            DebatesView.picture_url,
            DebatesView.end_at,
            DebatesView.created_at,
            DebatesView.created_by,
            DebatesView.leader,
            DebatesView.response_count,
        )
    )

    result = query.first()
    return result._asdict() if result else {}


def get_categories(session: Session) -> list[str]:
    """
    Returns list of categories
    """
    debate_categories = (
        session.query(DebateCategory).order_by(DebateCategory.name).all()
    )
    return [category.to_dict() for category in debate_categories]
