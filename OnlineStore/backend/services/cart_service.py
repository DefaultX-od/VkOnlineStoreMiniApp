from OnlineStore.backend.repositories import CartRepo
from OnlineStore.backend.models import *


class CartService:
    def __init__(self, product_service: ProductService):
        self.repo = CartRepo()
        self.product_service = product_service

    def get_total_items_count(self, user_id: float) -> int:
        cart = self._get_or_create_active_cart(user_id)
        if not cart:
            cart = self.repo.create_cart(user_id)
        items_count = self.repo.get_items_count(cart.id)
        return items_count


    def get_item_quantity(self, product_id: int, user_id: float) -> int:
        cart = self._get_or_create_active_cart(user_id)
        quantity = self.repo.get_cart_item_quantity(cart, product_id)
        return quantity or 0

    def deactivate_cart(self, cart: Cart) -> Cart:
        cart.is_active = 0

        for item in cart.cart_items:
            item.normal_price = item.product.price
            self.product_service.apply_discount_to_product(item.product)
            item.purchase_price = item.product.final_price
        cart = self.repo.update_cart(cart)
        return cart

    def _get_or_create_active_cart(self, user_id: float) -> Cart:
        cart = self.repo.get_active_cart(user_id)
        if cart:
            return cart
        else:
            cart = self.repo.create_cart(user_id)
        return cart

    def get_active_cart(self, user_id: float) -> Cart | None:
        cart = self.repo.get_active_cart(user_id)
        if cart:
            return cart
        else:
            return None

    def finalize_cart(self, cart: Cart) -> Cart:
        for item in cart.cart_items:
            self.product_service.finalize_product(item.product)
        self._set_cart_info(cart)
        return cart

    def retrieve_active_cart(self, user_id: float) -> dict:
        cart = self._get_or_create_active_cart(user_id)
        cart = self.finalize_cart(cart)
        return cart.to_dic()


    def add_to_cart(self, product_id: int, user_id: float):
        cart = self._get_or_create_active_cart(user_id)
        self.repo.add_item(product_id, cart)

    def delete_from_cart(self, item_id: int, user_id: float) -> int:
        cart = self.repo.get_active_cart(user_id)
        cart_item = self.repo.get_cart_item(item_id, cart)
        if cart and cart_item:
            return self.repo.delete_item(cart_item)
        return 0

    def increment_cart_item_quantity(self, item_id: int, user_id: float) -> int:
        cart = self.repo.get_active_cart(user_id)
        cart_item = self.repo.get_cart_item(item_id, cart)
        if cart.id == cart_item.cart_id:
            cart_item.quantity += 1
            return self.repo.update_cart_item_quantity(cart_item)
        return 0

    def decrement_cart_item_quantity(self, item_id: int, user_id: float) -> int:
        cart = self.repo.get_active_cart(user_id)
        cart_item = self.repo.get_cart_item(item_id, cart)
        if cart.id == cart_item.cart_id:
            cart_item.quantity -= 1
            return self.repo.update_cart_item_quantity(cart_item)
        return 0

    def clear_cart(self, user_id: float):
        cart = self.repo.get_active_cart(user_id)
        if cart:
            self.repo.delete_all_items(cart)

    def refresh_summary(self, user_id: float) -> dict:
        cart = self._get_or_create_active_cart(user_id)
        for item in cart.cart_items:
            self.product_service.finalize_product(item.product)
        self._set_cart_info(cart)
        return cart.to_dic()

    def _set_cart_info(self, cart: Cart) -> Cart:
        items_count = 0
        total_discount = 0
        full_price = 0
        total = 0

        for item in cart.cart_items:
            items_count += item.quantity
            if item.purchase_price and item.normal_price:
                total_discount +=(item.normal_price - item.purchase_price) * item.quantity
                total += item.purchase_price * item.quantity
                full_price += item.normal_price * item.quantity
            else:
                total_discount += (item.product.price - item.product.final_price) * item.quantity
                total += item.product.final_price * item.quantity
                full_price += item.product.price * item.quantity

        cart.items_count = items_count
        cart.total_discount = total_discount
        cart.full_price = full_price
        cart.total = total
        return cart
