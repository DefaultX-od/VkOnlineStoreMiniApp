from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from .base import Base

class CategoryDetail(Base):
    __tablename__ = 'category_details'

    id = Column(Integer, name='category_details_id', primary_key=True, autoincrement=True)
    name = Column(String(100), name='name')
    is_main = Column(Boolean, name='is_main')

    product_detail = relationship('ProductDetail', back_populates='category_detail')