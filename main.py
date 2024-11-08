from extract.nomenclatures import NomenclaturesFile
from extract.ozon_parser import OzonSellerParser
from services.price_data import PriceData
from transforms.price_transforms import PriceTransform

print(PriceData(OzonSellerParser, NomenclaturesFile, PriceTransform).price_data()[0])
