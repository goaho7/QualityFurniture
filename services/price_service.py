from extract.nomenclatures import NomenclaturesFile
from extract.ozon_parser import OzonSellerParser
from transforms.price_transforms import PriceTransform


class PriceService:
    def __init__(self, parser: OzonSellerParser, nomenclatures: NomenclaturesFile, transform: PriceTransform):
        self.parser = parser()
        self.nomenclatures = nomenclatures()
        self.transform = transform()

    def data(self):
        ozone_prices = self.parser.get_info_price()
        nomenclatures = self.nomenclatures.get_nomenclatures()
        products_in_all_actions = self.parser.products_in_all_actions()
        return self.transform.transform_ozone(ozone_prices, nomenclatures, products_in_all_actions)
