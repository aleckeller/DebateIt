"""
Routes for debate endpoints
"""
from aws_lambda_powertools.event_handler.api_gateway import Router

# pylint: disable=import-error

from .controller import get_debates

# pylint: enable=import-error

router = Router()


@router.get("/list")
def get_debates_view():
    """
    Returns list of debates
    """
    return get_debates(router.context["db_session"])
