import os
from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_HOST = os.getenv("DB_HOST", False)
DB_USER = os.getenv("DB_USER", False)
DB_PASSWORD = os.getenv("DB_PASSWORD", False)
DBNAME = "Spanglish"
MYSQL_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DBNAME}"
SQLITE_URL = "sqlite:///./sql_test_app.db"
SQLALCHEMY_DATABASE_URL = MYSQL_URL if DB_HOST else SQLITE_URL


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
