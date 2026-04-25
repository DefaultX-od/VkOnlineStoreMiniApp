from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base

class ProductDetail(Base):
    __tablename__ = 'item_details'

    id = Column(Integer, name='item_details_id', primary_key=True, autoincrement=True)
    category_details_id = Column(Integer, ForeignKey('category_details.category_details_id'))
    product_id = Column(Integer, name='item_id')
    value = Column(String(), name='value')

    category_detail = relationship('CategoryDetail', back_populates='product_detail')

    def to_dic(self):
        return {
            'name' : self.category_detail.name,
            'value' : self.value
        }