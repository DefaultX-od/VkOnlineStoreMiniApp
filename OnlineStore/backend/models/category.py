from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .base import Base

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, name='category_id', primary_key=True)
    name = Column(String(100), name='name', nullable=False)
    group_id = Column(Integer, ForeignKey('category_groups.category_group_id'), name='category_group_id')
    icon = Column(String(100), name='icon')
    is_hidden = Column(Boolean, name='is_hidden', default=False)

    group = relationship('CategoryGroup', back_populates='categories')
    products = relationship('Product', back_populates='category')

    def to_dic(self):
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon
        }