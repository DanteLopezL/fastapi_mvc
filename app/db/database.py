from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://localhost:5433/fastapi_db')

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

