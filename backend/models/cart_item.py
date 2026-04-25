from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from .base import Base

class CartItem(Base):
    __tablename__ = 'cart_details'

    id = Column(Integer, name='cart_details_id', primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.cart_id'), name='cart_id')
    product_id = Column(Integer, ForeignKey('items.item_id'), name='item_id')
    quantity = Column(Integer, name='quantity')
    normal_price = Column(Numeric(8, 2), name='normal_purchase_price')
    purchase_price = Column(Numeric(8,2), name='purchase_price')

    product = relationship('Product', back_populates='cart_item', lazy='joined')
    cart = relationship('Cart', back_populates='cart_items')

    def to_dic(self):
        return{
            'id' : self.id,
            'quantity' : self.quantity,
            'normal_price' : self.normal_price,
            'purchase_price' : self.purchase_price,
            'product' : self.product.to_dic()
        }

