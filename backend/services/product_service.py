from decimal import Decimal

from backend.repositories import ProductRepo
from .image_service import ImageService
from backend.models import *


class ProductService:
    def __init__(self):
        self.repo = ProductRepo()
        self.image_manager = ImageService()

    def retrieve_categories(self) -> dict:
        grouped_categories = self.repo.get_category_groups_detailed()
        dic = {}
        for group in grouped_categories:
            dic[group.id] = group.to_dic()
            for category in group.categories:
                self._set_category_icon(category)
                dic[group.id]['categories'].append(category.to_dic())
        return dic

    def retrieve_category(self, id: int) -> dict:
        grouped_products = self.repo.get_category(id)
        dic = {}
        for group in grouped_products:
            group.products = group.products[:2]
            if len(group.products) < 1:
                continue
            else:
                dic[group.id] = group.to_dic()
                for product in group.products:
                    self.finalize_product(product)
                    dic[group.id]['products'].append(product.to_dic())
        return dic

    def retrieve_group(self, group_id: int, category_id: int) -> dict:
        grouped_products = self.repo.get_group(group_id, category_id)
        dic = {}
        for group in grouped_products:
            dic[group.id] = group.to_dic()
            for product in group.products:
                self.finalize_product(product)
                dic[group.id]['products'].append(product.to_dic())
        return dic

    def retrieve_product(self, id: int) -> dict:
        product = self.repo.get_product_by_id(id)
        self.finalize_product(product)
        self._populate_details(product)
        dic = product.to_dic()
        dic['details']['mainDetails'] = [detail.to_dic() for detail in product.details[0]]
        dic['details']['subDetails'] = [detail.to_dic() for detail in product.details[1]]
        return dic

    def retrieve_favorites(self, user_id: float) -> dict:
        favorites: list[FavoriteItem] = self.repo.get_favorites_list(user_id)
        products: list[dict] = []
        for favorite in favorites:
            product: Product = favorite.product
            self.finalize_product(product)
            products.append(product.to_dic())
        return {
            '-1':{
                'id': -1,
                'name': 'Избранное',
                'products': products
            }
        }

    def finalize_product(self, product: Product):
        self.apply_discount_to_product(product)
        self._populate_album(product)
        self._set_main_img(product)

    def _set_category_icon(self, category: Category):
        category.icon = self.image_manager.get_image(category.icon)

    def _calculate_final_price(self, price: Decimal, discount: int) -> Decimal:
        return round(price - price * (Decimal(discount) / 100), 2)

    def apply_discount_to_product(self, product: Product):
        product.final_price = self._calculate_final_price(product.price, product.discount)

    def _populate_album(self, product: Product):
        product.album = self.image_manager.get_album(product.album_id)

    def _populate_details(self, product: Product):
        details = self.repo.get_product_details_by_product_id(product.id)
        details_main = []
        details_sub = []
        for detail in details:
            if detail.category_detail.is_main:
                details_main.append(detail)
            else:
                details_sub.append(detail)
        product.details = details_main, details_sub

    def _set_main_img(self, product: Product):
        if product.album is not None:
            product.main_img = product.album[0]

    def get_fav_status(self, id: int, user_id: float) -> bool:
        fav_item = self.repo.get_favorite_item(id, user_id)
        return True if fav_item else False

    def add_product_to_favorites(self, product_id: int, user_id: float) -> bool:
        product = self.repo.get_product_by_id(product_id)
        if product:
            fav_item = FavoriteItem(
                product_id=product.id,
                user_id=user_id
            )
            fav_item = self.repo.save_favorite_item(fav_item)
            return True if fav_item else False
        return False

    def delete_product_from_favorites(self, product_id, user_id):
        self.repo.remove_favorite_item(product_id, user_id)
        return False

    # Для бота

    # def get_main_categories(self):
    #     pass
    #
    # def get_categories_groups(self):
    #     pass
    #
    # def get_product_groups(self):
    #     pass
    #
    # def get_products(self):
    #     pass
    #
    # def get_category_details(self):
    #     pass

