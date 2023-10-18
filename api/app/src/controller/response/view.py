"""
Routes for response endpoints
"""
from aws_lambda_powertools.event_handler.api_gateway import Router

# pylint: disable=import-error

from .controller import (
    create_response,
    increment_debate_response_agree,
    decrement_debate_response_agree,
    increment_debate_response_disagree,
    decrement_debate_response_disagree,
)
from .model import CreateResponse

# pylint: enable=import-error

router = Router()


@router.post("")
def create_response_route():
    """
    Creates response
    """
    request_body = (
        router.current_event.json_body if router.current_event.get("body") else {}
    )

    response = create_response(
        router.context["db_session"],
        CreateResponse(
            body=request_body.get("body"),
            debate_id=request_body.get("debate_id"),
            created_by_id=request_body.get("created_by_id"),
            agree=0,
            disagree=0,
        ),
    )

    router.context["db_session"].commit()

    return response.to_dict()


@router.post("/<response_id>/agree")
def increment_debate_response_agree_route(response_id: int):
    """
    Increments agree vote on a debate response route
    """
    count = increment_debate_response_agree(router.context["db_session"], response_id)
    router.context["db_session"].commit()
    return count


@router.delete("/<response_id>/agree")
def decrements_debate_response_agree_route(response_id: int):
    """
    Decrements agree vote on a debate response route
    """
    count = decrement_debate_response_agree(router.context["db_session"], response_id)
    router.context["db_session"].commit()
    return count


@router.post("/<response_id>/disagree")
def increment_debate_response_disagree_route(response_id: int):
    """
    Increments disagree vote on a debate response route
    """
    count = increment_debate_response_disagree(
        router.context["db_session"], response_id
    )
    router.context["db_session"].commit()
    return count


@router.delete("/<response_id>/disagree")
def decrements_debate_response_disagree_route(response_id: int):
    """
    Decrements disagree vote on a debate response route
    """
    count = decrement_debate_response_disagree(
        router.context["db_session"], response_id
    )
    router.context["db_session"].commit()
    return count
