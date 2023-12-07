from os import environ

from aws_lambda_powertools.utilities.parameters import get_secret

from utils import create_db_engine, create_db_session
from controller import create_user
from model import CreateUser


def lambda_handler(event, context):
    """
    Perform post user sign up actions
    """
    db_session = _get_db_session(
        get_secret(environ["DB_SECRET_NAME"], transform="json")
    )
    user_id = create_user(
        db_session,
        CreateUser(
            id=event["request"]["userAttributes"]["sub"], username=event["userName"]
        ),
    )
    db_session.commit()
    return {"id": str(user_id)}


# Get SQLAlchemy Session
def _get_db_session(secret):
    username = secret["username"]
    password = secret["password"]
    db_name = secret["dbname"]
    host = secret["host"]

    db_conn_string = f"postgresql://{username}:{password}@{host}/{db_name}"

    engine = create_db_engine(db_conn_string)
    session = create_db_session(engine)
    return session
