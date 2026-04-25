from .cart_service import CartService
from backend.repositories import OrderRepo
from backend.models import *


class OrderService:
    def __init__(self, cart_service: CartService):
        self.repo = OrderRepo()
        self.cart_service = cart_service

    def retrieve_orders(self, user_id: float) -> list[dict]:
        orders_raw = self.repo.get_orders(user_id)
        orders = []
        for order in orders_raw:
            order.cart = self.cart_service.finalize_cart(order.cart)
            orders.append(order.to_dic())
        return orders

    def retrieve_orders_by_status(self, status_id: int) -> list[dict]:
        orders_raw = self.repo.get_orders_by_status(status_id)
        orders = []
        for order in orders_raw:
            order.cart = self.cart_service.finalize_cart(order.cart)
            orders.append(order.to_dic())
        return orders

    def retrieve_completed_orders(self) -> list[dict]:
        orders_raw = self.repo.get_completed_orders()
        orders = []
        for order in orders_raw:
            order.cart = self.cart_service.finalize_cart(order.cart)
            orders.append(order.to_dic())
        return orders

    def retrieve_canceled_orders(self) -> list[dict]:
        orders_raw = self.repo.get_canceled_orders()
        orders = []
        for order in orders_raw:
            order.cart = self.cart_service.finalize_cart(order.cart)
            orders.append(order.to_dic())
        return orders

    def retrieve_order(self, user_id: float, order_id: int) -> dict:
        order = self.repo.get_order_by_id(order_id)
        order.cart = self.cart_service.finalize_cart(order.cart)
        return order.to_dic()

    def create_order(self, user_id: float, cart: Cart, drop_point_id: int, payment_method_id: int) -> int:
        order_id = self.repo.create_order(user_id, cart, drop_point_id, payment_method_id)
        cart = self.cart_service.deactivate_cart(cart)
        return order_id

    def cancel_order(self, user_id: float, order_id: int) -> bool | None:
        order = self.repo.get_order_by_id(order_id)
        if order.user_id == float(user_id):
            return self.repo.cancel_order(order)
        else:
            return None

    def update_order(self, order_id: int, status_id: int, is_completed: bool) -> tuple[bool, float]:
        order = self.repo.get_order_by_id(order_id)
        if is_completed:
            res = self.repo.set_order_completed(order)
        else:
            res = self.repo.update_order_status(order, status_id)
        return res, order.user_id

    def retrieve_order_statuses(self) -> list[dict]:
        order_statuses = self.repo.get_all_order_statuses()
        res = []
        for status in order_statuses:
            res.append(status.to_dic())
        return res

    def retrieve_available_drop_points(self) -> list[dict]:
        drop_points = self.repo.get_drop_points(include_hidden=False)
        res = []
        for drop_point in drop_points:
            res.append(drop_point.to_dic())
        return res

    def retrieve_payment_methods(self) -> list[dict]:
        payment_methods = self.repo.get_payment_methods(include_hidden=False)
        res = []
        for pm in payment_methods:
            res.append(pm.to_dic())
        return res
