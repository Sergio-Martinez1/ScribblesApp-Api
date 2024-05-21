from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from .connection import settings
from google.cloud.sql.connector import Connector
# from google.oauth2 import service_account

# credentials = service_account.Credentials.from_service_account_file(
#     filename=settings.GOOGLE_APPLICATION_CREDENTIALS)

instance_conection_name = settings.INSTANCE_CONNECTION_NAME


def init_connection_pool(conector: Connector) -> Engine:

    def getconn():
        conn = conector.connect(instance_conection_name,
                                "pg8000",
                                enable_iam_auth=True,
                                user=settings.CLOUD_SQL_USER,
                                password=settings.CLOUD_SQL_PASSWORD,
                                db=settings.POSTGRES_DB,
                                ip_type="PRIVATE")
        return conn

    engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, creator=getconn)

    return engine


conector = Connector()

engine = init_connection_pool(conector)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
