import os
from click import echo
from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_HOST = None #os.getenv("DB_HOST", None)
DB_USER = os.getenv("DB_USER", None)
DB_PASSWORD = os.getenv("DB_PASSWORD", None)
POSTGRES_USER = os.getenv("POSTGRES_USER", None)
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", None)
POSTGRES_HOST = os.getenv("POSTGRES_HOST", None)
POSTGRES_PORT = os.getenv("POSTGRES_PORT", None)
POSTGRES_DB = os.getenv("POSTGRES_DB", None)
DBNAME = "Spanglish"
MYSQL_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DBNAME}"
POSTGRESQL_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
SQLITE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = MYSQL_URL if DB_HOST else SQLITE_URL


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={
        "check_same_thread": False
    }
)
# add echo=True to the create_engine to echo the db queries

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
