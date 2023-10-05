"""
Entrypoint for the API
"""
from os import environ

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

# pylint: disable=import-error
from src.controller.debate.view import router as debate_router

# pylint: enable=import-error
app = APIGatewayRestResolver()
app.include_router(debate_router, prefix="/debate")

LOGGER = Logger(level=environ["LOG_LEVEL"])


@LOGGER.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    """
    Router for the lambda API
    """

    LOGGER.debug(event)
    LOGGER.debug(context)
    app.append_context(logger=LOGGER)
    try:
        result = app.resolve(event, context)
        return result
    except ValueError as error:
        LOGGER.error(error)
        return {
            "statusCode": 400,
            "body": str(error),
        }


@app.get("/health")
def get_health() -> dict:
    """
    Health check endpoint
    """
    return {"statusCode": 200, "body": "OK"}
