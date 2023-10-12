"""
Insert test data
"""
from os import environ
from datetime import datetime, timedelta

from aws_lambda_powertools.utilities.parameters import get_secret
from sqlalchemy import insert, text, delete

from orm_layer.python.utils import create_db_engine, create_db_session
from orm_layer.python.models import (
    User,
    Debate,
    DebateCategory,
    debate_debate_category_table,
    Response,
)
from orm_layer.python.table_data import DEBATE_CATEGORIES


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
            {"username": "testuser1"},
            {"username": "testuser2"},
            {"username": "testuser3"},
            {"username": "testuser4"},
            {"username": "testuser5"},
        ],
    )


def _insert_debates():
    DB_SESSION.execute(
        insert(Debate),
        [
            {
                "title": "Should governments implement a universal basic income to provide financial support to all citizens, regardless of their employment status?",
                "summary": "This would list out any additional details a user wanted to provide for the debate",
                "created_by_id": 1,
                "end_at": datetime.now() + timedelta(days=3),
            },
            {
                "title": "Is the current global approach to combating climate change effective, or should there be a shift in focus or strategy?",
                "summary": "This would list out any additional details a user wanted to provide for the debate",
                "created_by_id": 2,
                "end_at": datetime.now() + timedelta(days=2),
            },
            {
                "title": "How should governments balance the need for online privacy rights with the necessity of national security surveillance programs?",
                "summary": "This would list out any additional details a user wanted to provide for the debate",
                "created_by_id": 1,
                "end_at": datetime.now() - timedelta(days=2),
                "winner_id": 2,
            },
            {
                "title": "Should governments legalize and regulate the recreational use of currently illegal drugs, such as marijuana or psychedelics?",
                "summary": "This would list out any additional details a user wanted to provide for the debate",
                "created_by_id": 3,
                "end_at": datetime.now(),
                "winner_id": 3,
            },
        ],
    )


def _insert_debate_categories():
    categories = [
        {"id": index + 1, "name": name} for index, name in enumerate(DEBATE_CATEGORIES)
    ]
    DB_SESSION.execute(
        insert(DebateCategory),
        categories,
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
                "body": "UBI can provide financial security to individuals and families living in poverty, helping them meet basic needs such as food, shelter, and healthcare.",
                "agree": 25,
                "disagree": 4,
                "debate_id": 1,
                "created_by_id": 1,
            },
            {
                "body": "UBI cannot provide financial security to individuals and families living in poverty, helping them meet basic needs such as food, shelter, and healthcare.",
                "agree": 3,
                "disagree": 25,
                "debate_id": 1,
                "created_by_id": 3,
            },
            {
                "body": "There has been a rapid expansion of renewable energy sources like solar and wind power, which contribute to reducing carbon emissions.",
                "agree": 2,
                "disagree": 2,
                "debate_id": 2,
                "created_by_id": 2,
            },
            {
                "body": "Ensure that these laws are regularly reviewed and updated to keep pace with technological advancements and changing security needs.",
                "agree": 13,
                "disagree": 0,
                "debate_id": 3,
                "created_by_id": 4,
            },
        ],
    )


table_names = [
    Debate.__table__,
    DebateCategory.__table__,
    f"public.{User.__table__}",
    Response.__table__,
]
for name in table_names:
    DB_SESSION.execute(text(f"TRUNCATE TABLE {name} CASCADE;"))
    DB_SESSION.execute(text(f"ALTER SEQUENCE {name}_id_seq RESTART WITH 1"))

_insert_users()
_insert_debates()
_insert_debate_categories()
_insert_debate_debate_category_relationships()
_insert_responses()

DB_SESSION.commit()
DB_SESSION.close()
