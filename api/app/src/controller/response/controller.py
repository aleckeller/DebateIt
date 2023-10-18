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


def increment_debate_response_agree(session: Session, response_id: int) -> int:
    """
    Increments agree vote on a debate response
    """
    response = _get_response(session, response_id)
    response.agree += 1
    return response.agree


def decrement_debate_response_agree(session: Session, response_id: int) -> int:
    """
    Decrements agree vote on a debate response
    """
    response = _get_response(session, response_id)
    response.agree -= 1
    return response.agree


def increment_debate_response_disagree(session: Session, response_id: int) -> int:
    """
    Increments disagree vote on a debate response
    """
    response = _get_response(session, response_id)
    response.disagree += 1
    return response.disagree


def decrement_debate_response_disagree(session: Session, response_id: int) -> int:
    """
    Decrements disagree vote on a debate response
    """
    response = _get_response(session, response_id)
    response.disagree -= 1
    return response.disagree


def _get_response(session: Session, response_id: int) -> Response:
    return session.query(Response).filter(Response.id == response_id).first()
