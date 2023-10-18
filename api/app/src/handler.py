"""
Entrypoint for the API
"""
from os import environ

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.parameters import get_secret
from boto3 import client

# pylint: disable=import-error
from src.controller.debate.view import router as debate_router
from src.controller.response.view import router as response_router
from src.service.files import FileService

from src.service.database import get_db_session

# pylint: enable=import-error
app = APIGatewayRestResolver()
app.include_router(debate_router, prefix="/debate")
app.include_router(response_router, prefix="/response")

LOGGER = Logger(level=environ["LOG_LEVEL"])
DB_SESSION = get_db_session(get_secret(environ["DB_SECRET_NAME"], transform="json"))
FILE_SERVICE = FileService(client("s3"), environ["S3_BUCKET"])


@LOGGER.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    """
    Router for the lambda API
    """

    LOGGER.debug(event)
    LOGGER.debug(context)
    app.append_context(logger=LOGGER, db_session=DB_SESSION, file_service=FILE_SERVICE)
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
