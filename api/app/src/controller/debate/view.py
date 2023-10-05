"""
Routes for debate endpoints
"""
from aws_lambda_powertools.event_handler.api_gateway import Router

# pylint: disable=import-error

# pylint: enable=import-error

router = Router()

@router.get("/list")
def get_debates():
    """
    Returns list of debates
    """
    router.context["logger"].info(router.context["db_session"])
    return []
