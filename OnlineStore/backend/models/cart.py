from sqlalchemy import Column, Integer, Double, Boolean
from sqlalchemy.orm import relationship

from .base import Base

class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, name='cart_id', primary_key=True)
    user_id = Column(Double, name='user_id')
    is_active = Column(Boolean, name='is_active')

    items_count = 0
    total_discount = 0.00
    total = 0.00
    full_price = 0.00

    cart_items = relationship('CartItem', back_populates='cart', lazy='joined')

    def to_dic(self):
        return{
            'id' : self.id,
            'items_count' : self.items_count,
            'total_discount' : self.total_discount,
            'total' : self.total,
            'full_price' : self.full_price,
            'items': [item.to_dic() for item in self.cart_items]
        }

