import logging

from extract.ozon_parser import OzonSellerParser
from repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)


class ProductService:
    def __init__(self, ozon_seller: OzonSellerParser, product_repository: ProductRepository):
        self.ozon_seller = ozon_seller()
        self.product_repository = product_repository()

    def update_products(self):
        """Обновить таблицу товаров"""
        product_list = self.ozon_seller.get_product_list()
        result = []
        for product_id in product_list:
            product_info = self.ozon_seller.get_product_info(product_id["product_id"])
            result.append(product_info)
        self.product_repository.update_product(result)
        logger.info("Товары обновлены")
