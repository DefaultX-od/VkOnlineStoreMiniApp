from sqlalchemy.orm import joinedload
from sqlalchemy import func

from OnlineStore.backend.models import Cart, CartItem
from OnlineStore.backend.services import DataBase


class CartRepo:
    def __init__(self):
        self.db = DataBase()

    def get_active_cart(self, user_id: float) -> Cart | None:
        with self.db.get_session() as db:
            cart = db.query(Cart).options(
                joinedload(Cart.cart_items)
                .joinedload(CartItem.product)
            ).filter(
                Cart.user_id==user_id, Cart.is_active==True
            ).first()
        return cart if cart else None

    def get_cart(self, id: int) -> Cart:
        with self.db.get_session() as db:
            cart = db.query(Cart).options(
                joinedload(Cart.cart_items)
                .joinedload(CartItem.product)
            ).filter(
                Cart.id == id
            ).first()
        return cart

    def create_cart(self, user_id: float) -> Cart:
        with self.db.get_session() as db:
            cart = Cart(
                user_id = user_id,
                is_active = True
            )
            db.add(cart)
            db.commit()
            db.refresh(cart)
        return cart

    def get_cart_item_quantity(self, cart: Cart, product_id: int) -> int:
        with self.db.get_session() as db:
            quantity = db.query(CartItem.quantity).filter(CartItem.cart_id==cart.id, CartItem.product_id==product_id).scalar()
        return quantity

    def add_item(self, product_id: int, cart: Cart):
        with self.db.get_session() as db:
            cart_item = CartItem(
                cart_id = cart.id,
                product_id = product_id,
                quantity = 1
            )
            db.add(cart_item)
            db.commit()
            db.refresh(cart_item)

    def get_cart_item(self, product_id: int, cart: Cart) -> CartItem:
        with self.db.get_session() as db:
            cart_item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id).first()
        return cart_item

    def update_cart(self, cart: Cart) -> Cart:
        with self.db.get_session() as db:
            db.add(cart)
            db.commit()
            db.refresh(cart)
        return cart

    def update_cart_item_quantity(self, cart_item: CartItem) -> int:
        with self.db.get_session() as db:
            db.add(cart_item)
            db.commit()
            db.refresh(cart_item)
        return cart_item.quantity

    def delete_item(self, item: CartItem) -> int:
        with self.db.get_session() as db:
            db.delete(item)
            db.commit()
        return 0

    def delete_all_items(self, cart: Cart):
        with self.db.get_session() as db:
            db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
            db.commit()

    def get_items_count(self, cart_id: int) -> int:
        with self.db.get_session() as db:
            items_count = db.query(func.sum(CartItem.quantity)).filter(CartItem.cart_id == cart_id).scalar()
        return int(items_count) if items_count else 0