from sqlalchemy.orm import joinedload

from backend.services import DataBase
from backend.models import *


class OrderRepo:
    def __init__(self):
        self.db = DataBase()

    def get_orders(self, user_id: float) -> list[Order]:
        with self.db.get_session() as db:
            orders = db.query(Order).options(
                joinedload(Order.cart).joinedload(Cart.cart_items).joinedload(CartItem.product)
            ).filter(Order.user_id == user_id).all()
        return orders

    def get_orders_by_status(self, status_id: int) -> list[Order]:
        with self.db.get_session() as db:
            orders = db.query(Order).options(
                joinedload(Order.cart).joinedload(Cart.cart_items).joinedload(CartItem.product)
            ).filter(Order.status_id == status_id, Order.is_completed == False, Order.is_canceled == False).all()
        for order in orders:
            print(order.is_canceled, order.is_completed)
        return orders

    def get_canceled_orders(self) -> list[Order]:
        with self.db.get_session() as db:
            orders = db.query(Order).options(
                joinedload(Order.cart).joinedload(Cart.cart_items).joinedload(CartItem.product)
            ).filter(Order.is_canceled == True).all()
        return orders

    def get_completed_orders(self) -> list[Order]:
        with self.db.get_session() as db:
            orders = db.query(Order).options(
                joinedload(Order.cart).joinedload(Cart.cart_items).joinedload(CartItem.product)
            ).filter(Order.is_completed == True).all()
        return orders


    def get_order_by_id(self, id: int) -> Order:
        with self.db.get_session() as db:
            order = db.query(Order).options(
                joinedload(Order.cart).joinedload(Cart.cart_items).joinedload(CartItem.product)
            ).filter(Order.id == id).first()
        return order

    def create_order(self, user_id: float, cart: Cart, drop_point_id: int, payment_method_id: int) -> int:
        with self.db.get_session() as db:
            order = Order(user_id=user_id, cart_id=cart.id, status_id=1, drop_point_id=drop_point_id, payment_method_id=payment_method_id)
            db.add(order)
            db.commit()
            db.refresh(order)
        return order.id

    def cancel_order(self, order: Order) -> bool:
        with self.db.get_session() as db:
            order.is_canceled = True
            db.add(order)
            db.commit()
            db.refresh(order)
        return order.is_canceled

    def update_order_status(self, order: Order, status_id: int) -> bool:
        order.status_id = status_id
        with self.db.get_session() as db:
            db.add(order)
            db.commit()
            db.refresh(order)
        return status_id == order.status_id

    def set_order_completed(self, order: Order) -> bool:
        order.is_completed = True
        with self.db.get_session() as db:
            db.add(order)
            db.commit()
            db.refresh(order)
        return order.is_completed == True

    def get_all_order_statuses(self) -> list[OrderStatus]:
        with self.db.get_session() as db:
            order_statuses = db.query(OrderStatus).all()
        return order_statuses

    def get_drop_points(self, include_hidden: bool = True) -> list[DropPoint]:
        with self.db.get_session() as db:
            query = db.query(DropPoint)
            if not include_hidden:
                query = query.filter(DropPoint.is_hidden == False)
        return query.all()

    def get_payment_methods(self, include_hidden: bool = True) -> list[PaymentMethod]:
        with self.db.get_session() as db:
            query = db.query(PaymentMethod)
            if not include_hidden:
                query = query.filter(PaymentMethod.is_hidden == False)
        return  query.all()

    def insert_drop_points(self, drop_points: list[DropPoint]):
        with self.db.get_session() as db:
            for dp in drop_points:
                db.merge(
                    DropPoint(
                        country=dp['country'],
                        city = dp['city'],
                        street=dp['street'],
                        building=dp['building'],
                        note=dp['notes'],
                        is_hidden=dp['is_hidden']
                    )
                )
            db.commit()

    def update_drop_points(self, drop_points: list[DropPoint]):
        with self.db.get_session() as db:
            for dp in drop_points:
                db.merge(
                    DropPoint(
                        id=dp['id'],
                        country=dp['country'],
                        city=dp['city'],
                        street=dp['street'],
                        building=dp['building'],
                        note=dp['notes'],
                        is_hidden=dp['is_hidden']
                    )
                )
            db.commit()