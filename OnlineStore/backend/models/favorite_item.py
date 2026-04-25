from sqlalchemy import Column, Integer, ForeignKey, Double
from sqlalchemy.orm import relationship

from .base import Base

class FavoriteItem(Base):
    __tablename__ = 'favorites'

    id = Column(Integer, name='favorite_id', primary_key=True)
    product_id = Column(Integer, ForeignKey('items.item_id'), name='item_id')
    user_id = Column(Double, name='user_id')

    product = relationship('Product', back_populates='fav_item')