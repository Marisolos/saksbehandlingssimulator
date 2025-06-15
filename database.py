from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Lager databasen og kobler til SQLite
engine = create_engine("sqlite:///cases.db", echo=False)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
