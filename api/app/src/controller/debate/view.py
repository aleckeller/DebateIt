"""
Routes for debate endpoints
"""
from datetime import datetime, timedelta

from aws_lambda_powertools.event_handler.api_gateway import Router

# pylint: disable=import-error

from .controller import (
    get_debates,
    create_debate,
)
from .model import CreateDebate

# pylint: enable=import-error

router = Router()


@router.get("/list")
def get_debates_route():
    """
    Returns list of debates
    """
    return get_debates(router.context["db_session"])


@router.post("")
def create_debate_route():
    """
    Creates debate
    """
    request_body = (
        router.current_event.json_body if router.current_event.get("body") else {}
    )

    id = create_debate(
        router.context["db_session"],
        CreateDebate(
            title=request_body.get("title"),
            summary=request_body.get("summary"),
            created_by_id=request_body.get("created_by_id"),
            end_at=request_body.get("end_at", datetime.now() + timedelta(days=7)),
            category_ids=request_body.get("category_ids"),
        ),
    )

    router.context["db_session"].commit()

    return {"id": id}
