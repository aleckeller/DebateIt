"""
Insert test data
"""
from os import environ
from datetime import datetime, timedelta

from aws_lambda_powertools.utilities.parameters import get_secret
from sqlalchemy import insert, delete

from orm_layer.python.utils import create_db_engine, create_db_session
from orm_layer.python.models import (
    User,
    Debate,
    DebateCategory,
    debate_debate_category_table,
    Response,
)


# Get SQLAlchemy Session
def get_db_session(secret):
    username = secret["username"]
    password = secret["password"]
    db_name = secret["dbname"]
    host = secret["host"]

    db_conn_string = f"postgresql://{username}:{password}@{host}/{db_name}"

    engine = create_db_engine(db_conn_string)
    session = create_db_session(engine)
    return session


DB_SESSION = get_db_session(
    get_secret(environ["DATABASE_SECRET_NAME"], transform="json")
)


def _insert_users():
    DB_SESSION.execute(
        insert(User),
        [
            {"id": 1, "username": "testuser1"},
            {"id": 2, "username": "testuser2"},
            {"id": 3, "username": "testuser3"},
            {"id": 4, "username": "testuser4"},
            {"id": 5, "username": "testuser5"},
        ],
    )


def _insert_debates():
    DB_SESSION.execute(
        insert(Debate),
        [
            {
                "id": 1,
                "title": "Should governments implement a universal basic income to provide financial support to all citizens, regardless of their employment status?",
                "summary": "This would list out any additional details a user wanted to provide for the debate",
                "created_by_id": 1,
                "end_at": datetime.now() + timedelta(days=3),
            },
            {
                "id": 2,
                "title": "Is the current global approach to combating climate change effective, or should there be a shift in focus or strategy?",
                "summary": "This would list out any additional details a user wanted to provide for the debate",
                "created_by_id": 2,
                "end_at": datetime.now() + timedelta(days=2),
            },
            {
                "id": 3,
                "title": "How should governments balance the need for online privacy rights with the necessity of national security surveillance programs?",
                "summary": "This would list out any additional details a user wanted to provide for the debate",
                "created_by_id": 1,
                "end_at": datetime.now() - timedelta(days=2),
                "winner_id": 2,
            },
            {
                "id": 4,
                "title": "Should governments legalize and regulate the recreational use of currently illegal drugs, such as marijuana or psychedelics?",
                "summary": "This would list out any additional details a user wanted to provide for the debate",
                "created_by_id": 3,
                "end_at": datetime.now(),
                "winner_id": 3,
            },
        ],
    )


def _insert_debate_categories():
    DB_SESSION.execute(
        insert(DebateCategory),
        [
            {"id": 1, "name": "Finance"},
            {"id": 2, "name": "Environment"},
            {"id": 3, "name": "Privacy"},
            {"id": 4, "name": "Drug Reform"},
        ],
    )


def _insert_debate_debate_category_relationships():
    DB_SESSION.execute(
        insert(debate_debate_category_table),
        [
            {"debate_id": 1, "debate_category_id": 1},
            {"debate_id": 2, "debate_category_id": 2},
            {"debate_id": 3, "debate_category_id": 3},
            {"debate_id": 4, "debate_category_id": 4},
        ],
    )


def _insert_responses():
    DB_SESSION.execute(
        insert(Response),
        [
            {
                "id": 1,
                "body": "UBI can provide financial security to individuals and families living in poverty, helping them meet basic needs such as food, shelter, and healthcare.",
                "agree": 25,
                "disagree": 4,
                "debate_id": 1,
                "user_id": 1,
            },
            {
                "id": 2,
                "body": "UBI cannot provide financial security to individuals and families living in poverty, helping them meet basic needs such as food, shelter, and healthcare.",
                "agree": 3,
                "disagree": 25,
                "debate_id": 1,
                "user_id": 3,
            },
            {
                "id": 3,
                "body": "There has been a rapid expansion of renewable energy sources like solar and wind power, which contribute to reducing carbon emissions.",
                "agree": 2,
                "disagree": 2,
                "debate_id": 2,
                "user_id": 2,
            },
            {
                "id": 4,
                "body": "Ensure that these laws are regularly reviewed and updated to keep pace with technological advancements and changing security needs.",
                "agree": 13,
                "disagree": 0,
                "debate_id": 3,
                "user_id": 4,
            },
        ],
    )


DB_SESSION.execute(delete(Response))
DB_SESSION.execute(delete(debate_debate_category_table))
DB_SESSION.execute(delete(Debate))
DB_SESSION.execute(delete(DebateCategory))
DB_SESSION.execute(delete(User))

_insert_users()
_insert_debates()
_insert_debate_categories()
_insert_debate_debate_category_relationships()
_insert_responses()

DB_SESSION.commit()
DB_SESSION.close()
