from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .base import Base

class PaymentMethod(Base):
    __tablename__ = 'payment_methods'

    id = Column(Integer, name='payment_method_id', primary_key=True)
    icon_id = Column(Integer, ForeignKey('generic_icons.icon_id'),name='icon_id')
    name = Column(String, name='name')
    description = Column(String, name='description')
    is_hidden = Column(Boolean, name='is_hidden')

    icon = relationship('GenericIcon', lazy='joined')

    def to_dic(self):
        return {
            'id': self.id,
            'text': self.name,
            'description': self.description,
            'icon': self.icon.link
        }
