"""
Routes for response endpoints
"""
from aws_lambda_powertools.event_handler.api_gateway import Router

# pylint: disable=import-error

from .controller import (
    create_response,
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
        ),
    )

    router.context["db_session"].commit()

    return response.to_dict()
