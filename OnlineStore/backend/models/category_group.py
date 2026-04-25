from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from .base import Base

class CategoryGroup(Base):
    __tablename__ = 'category_groups'

    id = Column(Integer, name='category_group_id', primary_key=True, autoincrement=True)
    name = Column(String(50), name='name', nullable=False)
    is_hidden = Column(Boolean, name='is_hidden', default=False)

    categories = relationship('Category', back_populates='group')

    def to_dic(self):
        return {
            'id': self.id,
            'name': self.name,
            'categories': []
        }