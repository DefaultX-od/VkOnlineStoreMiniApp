from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Numeric, Boolean, func
from sqlalchemy.orm import relationship

from .base import Base

class Product(Base):
    __tablename__ = 'items'

    id = Column(Integer, name='item_id', primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('categories.category_id'), name='category_id')
    group_id = Column(Integer, ForeignKey('item_groups.item_group_id'), name='item_group_id')
    name = Column(String(100), name='name', nullable=False)
    creation_date = Column(DateTime, name='creation_date', server_default=func.now())
    price = Column(Numeric(8,2), name='price')
    discount = Column(Integer, name='discount')
    album_id = Column(String(100), name='album')
    is_hidden = Column(Boolean, name='is_hidden', default=False)

    final_price = 0
    album = None
    main_img = None
    details = None

    group = relationship('ProductGroup', back_populates='products')
    category = relationship('Category', back_populates='products')
    cart_item = relationship('CartItem', back_populates='product')
    fav_item = relationship('FavoriteItem', back_populates='product')

    def to_dic(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'discount_price': self.final_price,
            'discount': self.discount,
            'album': self.album,
            'img' : self.main_img,
            'details' : {
                'mainDetails': [],
                'subDetails': []
            }
        }