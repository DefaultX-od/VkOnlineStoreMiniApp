from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from .base import Base

class ProductGroup(Base):
    __tablename__ = 'item_groups'

    id = Column(Integer, name='item_group_id', primary_key=True)
    name = Column(String(50), name='name', nullable=False)
    is_hidden = Column(Boolean, name='is_hidden', default=False)

    products = relationship('Product', back_populates='group')

    def to_dic(self):
        return {
            'id': self.id,
            'name': self.name,
            'products': []
        }