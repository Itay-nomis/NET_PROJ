from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base

# MySQL connection details
mysql_user = 'root'
mysql_password = 'password'
mysql_host = 'mysql'
mysql_database = 'project'
mysql_port = '3306'  # Default MySQL port

# Create the connection string for SQLAlchemy
connection_string = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}'

# Create the engine (this is the connection to the database)
engine = create_engine(connection_string)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False ,autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()