
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

from config import DATABASE_URL

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    boxhero_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    sku = Column(String)
    barcode = Column(String)
    photo_url = Column(String)
    cost = Column(String)
    price = Column(String)
    quantity = Column(Integer)
    attrs = Column(JSON)  # Store attributes as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SyncLog(Base):
    __tablename__ = 'sync_logs'

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    status = Column(String)
    records_processed = Column(Integer, default=0)
    error_message = Column(String)

def init_db():
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_pre_ping=True
    )
    Base.metadata.create_all(engine)
    return engine

def get_session():
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_pre_ping=True
    )
    Session = sessionmaker(bind=engine)
    return Session()
