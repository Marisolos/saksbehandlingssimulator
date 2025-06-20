from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Applicant(Base):
    __tablename__ = 'applicants'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    income = Column(Float)
    employment_status = Column(String)
    has_children = Column(Boolean)
    education_level = Column(String)  # "none", "highschool", "university"
    documentation_provided = Column(Boolean)
    cases = relationship("Case", back_populates="applicant")

class Case(Base):
    __tablename__ = 'cases'
    id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey('applicants.id'))
    status = Column(String)
    decision_reason = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    applicant = relationship("Applicant", back_populates="cases")