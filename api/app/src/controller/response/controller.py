from sqlalchemy import delete, func, insert, update
from sqlalchemy.orm import Session

from models import Response, Vote
from .model import CreateResponse, CreateVote, DeleteVote, UpdateVote


def create_response(session: Session, response: CreateResponse) -> int:
    """
    Creates a response
    """
    return session.execute(
        insert(Response).returning(Response),
        response.bind_vars(),
    ).first()[0]


def check_if_vote_exists(session: Session, vote_model: CreateVote) -> Vote:
    """
    Determines if a vote exists
    """
    return (
        session.query(Vote)
        .filter_by(
            created_by_id=vote_model.created_by_id,
            response_id=vote_model.response_id,
        )
        .first()
    )


def create_vote(session: Session, vote_model: CreateVote) -> int:
    """
    Creates a vote
    """
    return (
        session.execute(
            insert(Vote).returning(Vote),
            vote_model.bind_vars(),
        )
        .first()[0]
        .id
    )


def update_vote(session: Session, vote_model: UpdateVote):
    """
    Updates a vote
    """
    condition = Vote.id == vote_model.vote_id
    update_stmt = update(Vote).where(condition).values(vote_type=vote_model.vote_type)
    session.execute(update_stmt)


def delete_vote(session: Session, vote_model: DeleteVote):
    condition = Vote.id == vote_model.vote_id
    update_stmt = delete(Vote).where(condition)
    session.execute(update_stmt)


def get_response_vote_counts(session: Session, response_id: int) -> dict:
    vote_counts = (
        session.query(
            func.count().filter(Vote.vote_type == "agree").label("agree_count"),
            func.count().filter(Vote.vote_type == "disagree").label("disagree_count"),
        )
        .filter(Vote.response_id == response_id)
        .first()
    )
    return {"agree": vote_counts.agree_count, "disagree": vote_counts.disagree_count}
