"""
Insert test data
"""
from os import environ
from datetime import datetime, timedelta

from aws_lambda_powertools.utilities.parameters import get_secret
from sqlalchemy import insert, text

from orm_layer.python.utils import create_db_engine, create_db_session
from orm_layer.python.models import (
    User,
    Debate,
    DebateCategory,
    debate_debate_category_table,
    Response,
    Vote,
    VoteChoice,
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
                "summary": "This would provide financial security to individuals and families living in poverty.",
                "created_by_id": 1,
                "end_at": datetime.now() + timedelta(days=6),
                "picture_url": "https://picsum.photos/id/4/200",
            },
            {
                "title": "Is the current global approach to combating climate change effective, or should there be a shift in focus or strategy?",
                "summary": "Discussing the effectiveness of current climate change strategies.",
                "created_by_id": 2,
                "end_at": datetime.now() + timedelta(days=5),
                "picture_url": "https://picsum.photos/id/69/200",
            },
            {
                "title": "How should governments balance the need for online privacy rights with the necessity of national security surveillance programs?",
                "summary": "Exploring the delicate balance between privacy and security.",
                "created_by_id": 1,
                "end_at": datetime.now() + timedelta(days=1),
                "picture_url": "https://picsum.photos/id/154/200",
            },
            {
                "title": "Should governments legalize and regulate the recreational use of currently illegal drugs, such as marijuana or psychedelics?",
                "summary": "Examining the pros and cons of drug legalization.",
                "created_by_id": 3,
                "end_at": datetime.now() + timedelta(days=3),
                "picture_url": "https://picsum.photos/id/176/200",
            },
            {
                "title": "Is the death penalty an effective and just punishment for heinous crimes?",
                "summary": "Discussing the morality and effectiveness of the death penalty.",
                "created_by_id": 4,
                "end_at": datetime.now() + timedelta(days=9),
                "picture_url": "https://picsum.photos/id/21/200",
            },
            {
                "title": "Should students be required to wear uniforms in schools?",
                "summary": "Exploring the debate over school uniforms.",
                "created_by_id": 5,
                "end_at": datetime.now() + timedelta(days=1),
            },
            {
                "title": "Is social media doing more harm than good to society?",
                "summary": "Analyzing the impact of social media on society.",
                "created_by_id": 1,
                "end_at": datetime.now() + timedelta(days=1),
            },
            {
                "title": "Should professional athletes be allowed to kneel during the national anthem as a form of protest?",
                "summary": "Examining the role of athletes in social and political movements.",
                "created_by_id": 2,
                "end_at": datetime.now() + timedelta(days=2),
            },
            {
                "title": "Is censorship of art and media necessary to protect society from harmful content?",
                "summary": "Discussing the role of censorship in media and art.",
                "created_by_id": 3,
                "end_at": datetime.now() + timedelta(days=2),
                "picture_url": "https://picsum.photos/id/3/200",
            },
            {
                "title": "Should genetically modified organisms (GMOs) be allowed in the food supply?",
                "summary": "Debating the safety and benefits of GMOs in food.",
                "created_by_id": 4,
                "end_at": datetime.now() + timedelta(days=1),
            },
            {
                "title": "Is homeschooling a better option than traditional public education?",
                "summary": "Exploring the advantages and disadvantages of homeschooling.",
                "created_by_id": 5,
                "end_at": datetime.now() + timedelta(days=4),
                "picture_url": "https://picsum.photos/id/17/200",
            },
            {
                "title": "Should access to healthcare be considered a fundamental human right?",
                "summary": "Discussing the role of healthcare as a human right.",
                "created_by_id": 1,
                "end_at": datetime.now() + timedelta(days=6),
            },
            {
                "title": "Is space exploration a worthwhile investment for humanity?",
                "summary": "Examining the value of space exploration efforts.",
                "created_by_id": 2,
                "end_at": datetime.now() + timedelta(days=1),
                "picture_url": "https://picsum.photos/id/13/200",
            },
            {
                "title": "Should voting be mandatory for all eligible citizens?",
                "summary": "Debating whether voting should be compulsory.",
                "created_by_id": 3,
                "end_at": datetime.now() + timedelta(days=2),
            },
            {
                "title": "Should the legal drinking age be lowered or raised?",
                "summary": "Exploring the legal drinking age and its impact.",
                "created_by_id": 4,
                "end_at": datetime.now() + timedelta(days=5),
                "picture_url": "https://picsum.photos/id/99/200",
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
            {"debate_id": 5, "debate_category_id": 5},
            {"debate_id": 6, "debate_category_id": 6},
            {"debate_id": 7, "debate_category_id": 7},
            {"debate_id": 8, "debate_category_id": 8},
            {"debate_id": 9, "debate_category_id": 9},
            {"debate_id": 10, "debate_category_id": 10},
            {"debate_id": 11, "debate_category_id": 11},
            {"debate_id": 12, "debate_category_id": 12},
            {"debate_id": 13, "debate_category_id": 13},
            {"debate_id": 14, "debate_category_id": 14},
            {"debate_id": 15, "debate_category_id": 15},
        ],
    )


def _insert_responses():
    DB_SESSION.execute(
        insert(Response),
        [
            {
                "body": "A universal basic income (UBI) could provide financial security and eliminate poverty. It's a necessary step to ensure everyone's well-being.",
                "debate_id": 1,
                "created_by_id": 1,
            },
            {
                "body": "UBI may seem like a good idea, but it's fiscally irresponsible and can discourage people from working. It's not a practical solution.",
                "debate_id": 1,
                "created_by_id": 2,
            },
            {
                "body": "The current global approach to combating climate change is ineffective. We need a radical shift in strategy to address this urgent issue.",
                "debate_id": 2,
                "created_by_id": 3,
            },
            {
                "body": "We should continue with the current strategies and not make hasty changes. They are making a difference, albeit slowly.",
                "debate_id": 2,
                "created_by_id": 4,
            },
            {
                "body": "Online privacy is a fundamental right, and we should prioritize it over security. There are alternative ways to protect our nations.",
                "debate_id": 3,
                "created_by_id": 5,
            },
            {
                "body": "National security is paramount, and privacy rights need to be sacrificed for the greater good. We must protect our nations.",
                "debate_id": 3,
                "created_by_id": 1,
            },
            {
                "body": "Legalizing and regulating currently illegal drugs can reduce crime and create new sources of revenue for governments.",
                "debate_id": 4,
                "created_by_id": 2,
            },
            {
                "body": "Drug legalization can lead to increased addiction and societal problems. It's a dangerous path to take.",
                "debate_id": 4,
                "created_by_id": 3,
            },
            {
                "body": "The death penalty is inhumane and ineffective. It should be abolished in all civilized societies.",
                "debate_id": 5,
                "created_by_id": 4,
            },
            {
                "body": "The death penalty is a necessary punishment for the most heinous crimes. It serves as a deterrent and justice for the victims.",
                "debate_id": 5,
                "created_by_id": 5,
            },
            {
                "body": "Students should be required to wear uniforms in schools to promote discipline and reduce peer pressure based on clothing.",
                "debate_id": 6,
                "created_by_id": 1,
            },
            {
                "body": "School uniforms stifle individuality and self-expression. Students should have the freedom to choose their clothing.",
                "debate_id": 6,
                "created_by_id": 2,
            },
            {
                "body": "Social media is causing harm by promoting unrealistic standards and addictive behaviors. It's damaging society.",
                "debate_id": 7,
                "created_by_id": 3,
            },
            {
                "body": "Social media has connected people and allowed for the free exchange of ideas. It's a force for good in society.",
                "debate_id": 7,
                "created_by_id": 4,
            },
            {
                "body": "Professional athletes have the right to kneel during the national anthem to protest social injustice. It's an important form of expression.",
                "debate_id": 8,
                "created_by_id": 5,
            },
            {
                "body": "Athletes should not mix sports and politics. Kneeling during the national anthem is disrespectful to the country.",
                "debate_id": 8,
                "created_by_id": 1,
            },
            {
                "body": "Censorship of art and media is essential to protect society from harmful content, especially for children.",
                "debate_id": 9,
                "created_by_id": 2,
            },
            {
                "body": "Censorship limits creativity and infringes on freedom of expression. It's not the solution to societal problems.",
                "debate_id": 9,
                "created_by_id": 3,
            },
            {
                "body": "Genetically modified organisms (GMOs) have the potential to solve world hunger and improve crop yields. They should be allowed in the food supply.",
                "debate_id": 10,
                "created_by_id": 4,
            },
            {
                "body": "GMOs can have unknown health risks, and we should prioritize natural, organic food. They should not be allowed in the food supply.",
                "debate_id": 10,
                "created_by_id": 5,
            },
            {
                "body": "Homeschooling provides a more personalized and effective education. It should be a viable alternative to traditional public education.",
                "debate_id": 11,
                "created_by_id": 1,
            },
            {
                "body": "Traditional public education is essential for socialization and standardized learning. Homeschooling is not a better option.",
                "debate_id": 11,
                "created_by_id": 2,
            },
            {
                "body": "Access to healthcare is a fundamental human right. Every individual deserves equal and affordable healthcare.",
                "debate_id": 12,
                "created_by_id": 3,
            },
            {
                "body": "Healthcare is a service, not a right. The government should not be responsible for providing healthcare to everyone.",
                "debate_id": 12,
                "created_by_id": 4,
            },
            {
                "body": "Space exploration is a worthwhile investment that drives scientific progress and offers potential benefits for humanity.",
                "debate_id": 13,
                "created_by_id": 5,
            },
            {
                "body": "Space exploration is a costly endeavor with limited practical benefits for Earth. It's not a worthwhile investment.",
                "debate_id": 13,
                "created_by_id": 1,
            },
            {
                "body": "Voting should be mandatory for all eligible citizens to ensure full participation in democracy and representation.",
                "debate_id": 14,
                "created_by_id": 2,
            },
            {
                "body": "Mandatory voting infringes on individual freedom. Citizens should have the choice to participate or abstain.",
                "debate_id": 14,
                "created_by_id": 3,
            },
            {
                "body": "The legal drinking age should be lowered to encourage responsible drinking and reduce underage alcohol-related issues.",
                "debate_id": 15,
                "created_by_id": 4,
            },
            {
                "body": "Raising the legal drinking age can help protect young people from the harms of alcohol and reduce accidents.",
                "debate_id": 15,
                "created_by_id": 5,
            },
        ],
    )


def _insert_response_votes():
    DB_SESSION.execute(
        insert(Vote),
        [
            {
                "response_id": 1,
                "created_by_id": 1,
                "vote_type": VoteChoice.agree,
            },
            {
                "response_id": 2,
                "created_by_id": 1,
                "vote_type": VoteChoice.disagree,
            },
            {
                "response_id": 1,
                "created_by_id": 2,
                "vote_type": VoteChoice.disagree,
            },
        ],
    )


table_names = [
    Debate.__table__,
    DebateCategory.__table__,
    f"public.{User.__table__}",
    Response.__table__,
    Vote.__table__,
]
for name in table_names:
    DB_SESSION.execute(text(f"TRUNCATE TABLE {name} CASCADE;"))
    DB_SESSION.execute(text(f"ALTER SEQUENCE {name}_id_seq RESTART WITH 1"))

_insert_users()
_insert_debates()
_insert_debate_categories()
_insert_debate_debate_category_relationships()
_insert_responses()
_insert_response_votes()

DB_SESSION.commit()
DB_SESSION.close()
