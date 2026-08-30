from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
Base = declarative_base()

class Product(Base):
    __tablename__ = "PRODUCT"
    id = Column(Integer, primary_key=True, index= True)
    name = Column(String(20))
    description= Column(String(40))
    price= Column(Float)
    quantity=Column(Integer)
