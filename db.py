from datetime import datetime
from sqlalchemy import create_engine, Integer, String, Float, Column, Date
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///test.db")

Base = declarative_base()

class Stats(Base):
    __tablename__ = 'stats'
    id = Column(Integer, primary_key=True)
    date = Column(Date(), default=datetime.now)
    company = Column(String(16), nullable=False)
    q = Column(String(16), nullable=False)
    data = Column(String(16), nullable=False)
    total = Column(Float(200), nullable=False)    

Base.metadata.create_all(engine)

