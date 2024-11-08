from extract.nomenclatures import NomenclaturesFile
from extract.ozon_parser import OzonSellerParser
from transforms.price_transforms import PriceTransform


class PriceData:
    def __init__(self, parser: OzonSellerParser, nomenclatures: NomenclaturesFile, transform: PriceTransform):
        self.parser = parser()
        self.nomenclatures = nomenclatures()
        self.transform = transform()

    def price_data(self):
        ozone_prices = self.parser.get_info_price()
        nomenclatures = self.nomenclatures.get_nomenclatures()
        return self.transform.transform_ozone(ozone_prices, nomenclatures)
