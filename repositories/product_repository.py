from sqlalchemy.dialects.sqlite import insert

from models import Product, sqlite_session


class ProductRepository:
    model = Product

    def get_product(self):
        """Получить товары"""
        with sqlite_session() as session:
            query = session.query(self.model)
            return query.all()

    def update_product(self, data: list):
        """Обновление таблицы товаров"""
        with sqlite_session() as session:
            for product in data:
                insert_stmt = insert(self.model).values(
                    name=product["name"],
                    external_id=product["id"],
                    offer_id=product["offer_id"],
                    barcode=product["barcode"],
                    barcodes=product["barcodes"],
                    sku=product["sku"],
                    stocks=product["stocks"],
                )
                on_conflict_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=["external_id"],
                    set_={
                        "name": product["name"],
                        "external_id": product["id"],
                        "offer_id": product["offer_id"],
                        "barcode": product["barcode"],
                        "barcodes": product["barcodes"],
                        "sku": product["sku"],
                        "stocks": product["stocks"],
                    },
                )
                session.execute(on_conflict_stmt)
            session.commit()
