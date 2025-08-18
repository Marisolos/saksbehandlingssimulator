from models import Base
from sqlalchemy import create_engine
import os

if os.path.exists("cases.db"):
    os.remove("cases.db")

engine = create_engine("sqlite:///cases.db")
Base.metadata.create_all(bind=engine)
print("✅ Databasen er nullstilt.")

