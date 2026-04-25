from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class OrderStatus(Base):
    __tablename__ = 'order_statuses'
    id = Column(Integer, name='status_id', primary_key=True)
    icon_id = Column(Integer, ForeignKey('generic_icons.icon_id'),name='icon_id')
    name = Column(String, name='name')
    description = Column(String, name='description')

    icon = relationship('GenericIcon', lazy='joined')

    def to_dic(self):
        return{
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon.link
        }