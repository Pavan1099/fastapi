from sqlalchemy import Column, Integer, String, Float
from database import Base
from pydantic import BaseModel


# SQLAlchemy Model
class ProductDB(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, unique=True)
    description = Column(String(255))
    price = Column(Float)
    quantity = Column(Integer)


# Pydantic Models
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
