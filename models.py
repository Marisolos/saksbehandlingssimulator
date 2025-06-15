from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Applicant(Base):
    __tablename__ = 'applicants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    income = Column(Float)
    employment_status = Column(String)  # e.g., 'unemployed', 'employed'

class Case(Base):
    __tablename__ = 'cases'

    id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey('applicants.id'))
    status = Column(String)  # 'under_review', 'approved', 'rejected'
    created_at = Column(DateTime, default=datetime.utcnow)
    decision_reason = Column(String)
