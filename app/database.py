from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Make sure this is a full connection string like:
# postgresql://user:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL")

# PostgreSQL doesn't use check_same_thread
engine = create_engine(DATABASE_URL)

# Standard SQLAlchemy session setup
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
