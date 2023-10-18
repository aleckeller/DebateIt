"""
Routes for debate endpoints
"""
from base64 import b64decode
from datetime import datetime, timedelta

from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.exceptions import BadRequestError

# pylint: disable=import-error

from .controller import (
    get_debates,
    create_debate,
    update_file_location,
    upload_file,
    create_response,
    get_debate,
)
from .model import CreateDebate, UploadFile, CreateResponse, GetDebate

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


@router.put("/<debate_id>/file")
def put_file_route(debate_id: int):
    """
    Uploads picture for debate
    """
    if not router.current_event.get("body"):
        raise BadRequestError(msg="Must provide file in body")
    file_location = f"debates/pictures/{debate_id}"
    upload_file_model = UploadFile(
        debate_id=debate_id,
        file_location=file_location,
        file_bytes=b64decode(router.current_event.body),
    )

    response = upload_file(router.context["file_service"], upload_file_model)
    upload_file_model.file_location = (
        f"https://{response['bucket_name']}.s3.amazonaws.com/{file_location}"
    )
    update_file_location(
        upload_file_model,
        router.context["db_session"],
    )

    router.context["db_session"].commit()
    return {"picture_url": upload_file_model.file_location}


@router.post("/response")
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


@router.get("/<debate_id>/single")
def get_debate_route(debate_id: int):
    """
    Returns single debate
    """
    return get_debate(router.context["db_session"], GetDebate(debate_id=debate_id))
