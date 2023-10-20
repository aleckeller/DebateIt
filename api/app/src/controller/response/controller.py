from sqlalchemy import insert
from sqlalchemy.orm import Session

from models import Response
from .model import CreateResponse


def create_response(session: Session, response: CreateResponse) -> int:
    """
    Creates a response
    """
    return session.execute(
        insert(Response).returning(Response),
        response.bind_vars(),
    ).first()[0]


# def _get_response(session: Session, response_id: int) -> Response:
#     return session.query(Response).filter(Response.id == response_id).first()


# def _create_vote(session: Session, response_id: int, vote_choice: str):
#     return session.execute(
#         insert(Vote).returning(Vote),
#         {},
#     ).first()[0]
