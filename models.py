
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine, JSON, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

from config import DATABASE_URL

Base = declarative_base()

class Product(Base):
    __tablename__ = 'shopify_products'
    
    id = Column(Integer, primary_key=True)
    shopify_id = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    sku = Column(String)
    barcode = Column(String)
    inventory_quantity = Column(Integer, default=0)
    price = Column(Numeric(10, 2))
    compare_at_price = Column(Numeric(10, 2))
    image_url = Column(String)
    last_synced_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Sale(Base):
    __tablename__ = 'sales'
    
    id = Column(Integer, primary_key=True)
    shopify_order_id = Column(String, unique=True, nullable=False)
    order_name = Column(String)
    created_at = Column(DateTime)
    total_price = Column(Numeric(10, 2))
    synced_at = Column(DateTime, default=datetime.utcnow)

class SaleItem(Base):
    __tablename__ = 'sale_items'
    
    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey('sales.id'), nullable=False)
    title = Column(String, nullable=False)
    quantity = Column(Integer)
    original_price = Column(Numeric(10, 2))
    discounted_price = Column(Numeric(10, 2))
    sku = Column(String)
    sale = relationship("Sale", backref="items")

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
