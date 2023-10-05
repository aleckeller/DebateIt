from utils import create_db_engine, create_db_session

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