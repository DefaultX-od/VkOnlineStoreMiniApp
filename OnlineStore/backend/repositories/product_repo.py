from sqlalchemy.orm import joinedload

from OnlineStore.backend.services import DataBase


class ProductRepo():
    def __init__(self):
        self.db = DataBase()

    def get_category_groups_detailed(self) -> list[Category]:
        with self.db.get_session() as db:
            categories = db.query(CategoryGroup).options(
                joinedload(CategoryGroup.categories)
            ).all()
        return categories

    def get_category(self, id: int) -> list[ProductGroup]:
        with self.db.get_session() as db:
            grouped_products = (
                db.query(ProductGroup)
                .filter(ProductGroup.products.any(Product.category_id == id) & (Product.is_hidden == False))
                .options(joinedload(ProductGroup.products.and_(Product.category_id == id, Product.is_hidden == False))
                )
                .all()
            )
        return grouped_products


    def get_group(self, group_id: int, category_id: int) -> list[ProductGroup]:
        with self.db.get_session() as db:
            grouped_products = (
                db.query(ProductGroup)
                .options(
                    joinedload(ProductGroup.products.and_(Product.category_id == category_id, Product.is_hidden == False))
                )
                .filter(ProductGroup.id == group_id)
                .all()
            )
        return grouped_products

    def get_product_by_id(self, id: int) -> Product:
        with self.db.get_session() as db:
            product = db.query(Product).filter(Product.id == id).first()
        return product

    def get_product_details_by_product_id(self, id: int) -> list[ProductDetail]:
        with self.db.get_session() as db:
            details = db.query(ProductDetail).filter(
                ProductDetail.product_id == id
            ).options(
                joinedload(ProductDetail.category_detail)
            ).all()
        return details

    def get_favorite_item(self, product_id: int, user_id: float) -> FavoriteItem :
        with self.db.get_session() as db:
            fav_item = db.query(FavoriteItem).filter(FavoriteItem.product_id == product_id, FavoriteItem.user_id == user_id).first()
            return fav_item

    def get_favorites_list(self, user_id: float) -> list[FavoriteItem]:
        with self.db.get_session() as db:
            favorites = db.query(FavoriteItem).filter(FavoriteItem.user_id == user_id).options(joinedload(FavoriteItem.product)).all()
            return favorites

    def save_favorite_item(self, fav_item: FavoriteItem) -> FavoriteItem:
        with self.db.get_session() as db:
            db.add(fav_item)
            db.commit()
            db.refresh(fav_item)
        return fav_item

    def remove_favorite_item(self, product_id: int, user_id: float):
        fav_item = self.get_favorite_item(product_id, user_id)
        with self.db.get_session() as db:
            db.delete(fav_item)
            db.commit()

    def get_newest(self) -> list[Product]:
        pass

    def get_discounted(self) -> list[Product]:
        pass

    # Для бота

    def get_category_groups(self) -> list[CategoryGroup]:
        with self.db.get_session() as db:
            category_groups = db.query(CategoryGroup).all()
        return category_groups

    def get_product_groups(self) -> list[ProductGroup]:
        with self.db.get_session() as db:
            product_groups = db.query(ProductGroup).all()
        return product_groups
        pass

    def get_categories(self) -> list[Category]:
        with self.db.get_session() as db:
            categories = db.query(Category).options(
                joinedload(Category.group)
            ).all()
        return categories

    def get_products(self) -> list[Product]:
        with self.db.get_session() as db:
            products = db.query(Product).options(
                joinedload(Product.category),
                joinedload(Product.group)
            ).all()
        for p in products:
            p.details = self.get_product_details_by_product_id(p.id)
        return products

    def get_category_details(self) -> list[CategoryDetail]:
        with self.db.get_session() as db:
            category_details = db.query(CategoryDetail).all()
        return category_details

    def insert_category_groups(self, category_groups: list[CategoryGroup]):
        with self.db.get_session() as db:
            for cg in category_groups:
                db.merge(CategoryGroup(name=cg['name'], is_hidden=cg['is_hidden']))
            db.commit()

    def update_category_groups(self, category_groups: list[CategoryGroup]):
        with self.db.get_session() as db:
            for cg in category_groups:
                db.merge(CategoryGroup(id=cg['id'], name=cg['name'], is_hidden=cg['is_hidden']))
            db.commit()

    def insert_categories(self, categories: list[Category]):
        with self.db.get_session() as db:
            for c in categories:
                db.add(Category(name=c['name'],group_id=c['group'], icon=c['album'], is_hidden=c['is_hidden']))
            db.commit()

    def update_categories(self, categories: list[Category]):
        with self.db.get_session() as db:
            for c in categories:
                db.add(Category(id=c['id'], name=c['name'], group_id=c['group'], icon=c['album'], is_hidden=c['is_hidden']))
            db.commit()

    def insert_product_groups(self, product_groups: list[ProductGroup]):
        with self.db.get_session() as db:
            for pg in product_groups:
                db.add(ProductGroup(name=pg['name'],is_hidden=pg['is_hidden']))
            db.commit()

    def update_product_groups(self, product_groups: list[ProductGroup]):
        with self.db.get_session() as db:
            for pg in product_groups:
                db.add(ProductGroup(id=pg['id'],name=pg['name'],is_hidden=pg['is_hidden']))
            db.commit()

    def insert_products(self, products: list[Product]):
        with self.db.get_session() as db:
            for product in products:
                product_record = db.merge(
                    Product(
                        category_id=product['category'],
                        group_id=product['group'],
                        name=product['name'],
                        price=product['price'],
                        discount=product['discount'],
                        album_id=product['album'],
                        is_hidden=product['is_hidden']
                    )
                )
                db.flush()
                for detail in product['details']:
                    db.merge(
                        ProductDetail(
                            category_details_id=detail['id'],
                            product_id=product_record.id,
                            value=detail['value']
                        )
                    )
                db.commit()

    def update_products(self, products: list[Product]):
        with self.db.get_session() as db:
            for product in products:
                db.merge(
                    Product(
                        id=product['id'],
                        category_id=product['category'],
                        group_id=product['group'],
                        name=product['name'],
                        price=product['price'],
                        discount=product['discount'],
                        album_id=product['album'],
                        is_hidden=product['is_hidden']
                    )
                )

                existing_details = self.get_product_details_by_product_id(product['id'])
                incoming_details_ids = [d['id'] for d in product['details']]

                for detail in existing_details:
                    if detail.category_details_id not in incoming_details_ids:
                        db.delete(detail)

                existing_map = {d.category_details_id: d for d in existing_details}

                for detail in product['details']:

                    target_id = detail['id']

                    if detail['id'] in existing_map:
                        product_detail = ProductDetail(
                            id=existing_map[target_id].id,
                            category_details_id=detail['id'],
                            product_id=product['id'],
                            value=detail['value']
                        )
                    else:
                        product_detail = ProductDetail(
                            category_details_id=detail['id'],
                            product_id=product['id'],
                            value=detail['value']
                        )
                    db.merge(product_detail)
            db.commit()

    def insert_category_details(self, category_details: list[CategoryDetail]):
        with self.db.get_session() as db:
            for cd in category_details:
                db.add(CategoryDetail(name=cd['name'], is_main=cd['is_main']))
            db.commit()

    def update_category_details(self, category_details: list[CategoryDetail]):
        with self.db.get_session() as db:
            for cd in category_details:
                db.merge(CategoryDetail(id=cd['id'],name=cd['name'], is_main=cd['is_main']))
            db.commit()