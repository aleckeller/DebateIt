from logging.config import fileConfig
from os import environ

from sqlalchemy import create_engine

from alembic import context
from aws_lambda_powertools.utilities.parameters import get_secret
from alembic_utils.replaceable_entity import register_entities

from db.migrations.views import debates_view, responses_view
from db.migrations.functions import (
    update_leader_function,
    update_leader_on_vote_creation_trigger,
)

register_entities(
    [
        debates_view,
        responses_view,
        update_leader_function,
        update_leader_on_vote_creation_trigger,
    ]
)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from orm_layer.python.models import Base

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = _get_connection_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    url = _get_connection_url()
    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


def _get_connection_url() -> str:
    secret = get_secret(environ["DATABASE_SECRET_NAME"], transform="json")
    username = secret["username"]
    password = secret["password"]
    db_name = secret["dbname"]
    host = secret["host"]

    return f"postgresql://{username}:{password}@{host}/{db_name}"


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
