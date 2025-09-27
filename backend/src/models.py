from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    msisdn = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    
class Consumption(Base):
    __tablename__ = "consumption"
    id = Column(Integer, primary_key=True, autoincrement=True)
    msisdn = Column(String(20), index=True, nullable=False)
    balance = Column(Float, default=0.0)
    data_mb = Column(Float, default=0.0)
    minutes = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)