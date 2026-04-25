from sqlalchemy import Column, Integer, Double, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, name='order_id', primary_key=True)
    user_id = Column(Double, name='user_id')
    cart_id = Column(Integer, ForeignKey('carts.cart_id'),name='cart_id')
    status_id = Column(Integer, ForeignKey('order_statuses.status_id'),name='status_id')
    drop_point_id = Column(Integer, ForeignKey('drop_points.drop_point_id'), name='drop_point_id')
    payment_method_id = Column(Integer, ForeignKey('payment_methods.payment_method_id'), name='payment_method_id')
    creation_date = Column(DateTime, name='creation_date', server_default=func.now())
    is_paid = Column(Boolean, name='is_paid', default=False)
    is_completed = Column(Boolean, name='is_completed', default=False)
    is_canceled = Column(Boolean, name='is_canceled', default=False)

    cart = relationship('Cart', lazy='joined')
    payment_method = relationship('PaymentMethod', lazy='joined')
    drop_point = relationship('DropPoint', lazy='joined')
    status = relationship('OrderStatus', lazy='joined')

    def to_dic(self):
        return{
            'id' : self.id,
            'status_id' : self.status_id,
            'status': self.status.name,
            'drop_point' : self.drop_point.to_dic(),
            'payment_method' : self.payment_method.to_dic(),
            'date': self.creation_date.strftime('%d.%m.%Y'),
            'is_completed' : self.is_completed,
            'is_canceled' : self.is_canceled,
            'cart' : self.cart.to_dic()
        }