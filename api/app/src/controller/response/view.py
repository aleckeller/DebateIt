"""
Routes for response endpoints
"""
from aws_lambda_powertools.event_handler.api_gateway import Router

# pylint: disable=import-error

from .controller import (
    check_if_vote_exists,
    create_response,
    create_vote,
    get_response_vote_counts,
    update_vote,
    delete_vote,
)
from models import VoteChoice
from .model import CreateResponse, CreateVote, DeleteVote, UpdateVote

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
            # Replace below once authentication is implemented
            created_by_id=1,
        ),
    )

    router.context["db_session"].commit()

    return {
        **response.to_dict(),
        "agree": 0,
        "agreeEnabled": True,
        "disagree": 0,
        "disagreeEnabled": True,
    }


@router.post("/<response_id>/vote")
def vote_route(response_id: int):
    """
    Create, update, or delete a vote
    If vote does not exist, create it
    If vote exists but choice is different, update
    If vote exists but choice is not different, delete
    """
    parameters = router.current_event.get("queryStringParameters") or {}
    session = router.context["db_session"]

    vote_type = parameters.get("vote_type")
    vote = CreateVote(
        response_id=response_id,
        created_by_id=1,  # TODO: Update this when authentication is implemented
        vote_type=vote_type,
    )
    existing_vote = check_if_vote_exists(session, vote)
    vote_id = None
    agree_enabled = vote_type != VoteChoice.agree.value
    disagree_enabled = vote_type != VoteChoice.disagree.value
    if existing_vote:
        if existing_vote.vote_type.value == vote_type:
            delete_vote(session, DeleteVote(vote_id=existing_vote.id))
            agree_enabled = True
            disagree_enabled = True
        else:
            update_vote(
                session, UpdateVote(vote_id=existing_vote.id, vote_type=vote_type)
            )
        vote_id = existing_vote.id
    else:
        vote_id = create_vote(session, vote)

    vote_counts = get_response_vote_counts(session, response_id)

    session.commit()

    return {
        "vote_id": vote_id,
        "agree": {"count": vote_counts["agree"], "enabled": agree_enabled},
        "disagree": {"count": vote_counts["disagree"], "enabled": disagree_enabled},
    }
