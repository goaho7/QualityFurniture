from datetime import datetime

from extract.nomenclatures import NomenclaturesFile
from extract.ozon_parser import OzonSellerParser
from settings import FILE_HEADERS


class ExcelService:
    def __init__(self, ozon_seller: OzonSellerParser, nomenclatures: NomenclaturesFile):
        self.ozon_seller = ozon_seller()
        self.nomenclatures = nomenclatures()

    @staticmethod
    def str_to_float(string):
        """Преобразует строку в тип foat"""
        return float(string.replace(",", ".")) if string else None

    def products_in_all_actions(self) -> dict:
        """Возвращает словарь где ключ это product_id, а значение - список акций в которых участвует товар"""
        res = {}
        for action in self.ozon_seller.get_actions_list():
            for products in self.ozon_seller.get_list_products_in_actions(action["id"]):
                res.setdefault(products["id"], []).append(action["title"])
        return res

    def data_for_excel_file(self):
        """формирование данных для эксель файла"""
        ozone_prices = self.ozon_seller.get_info_price()  # Получаем список с информацией о ценах товара
        nomenclatures = self.nomenclatures.get_nomenclatures()  # Получаем данные из справочника номенклатур
        products_in_all_actions = self.products_in_all_actions()  # Cписок акций в которых участвует товар

        result = []
        for i in ozone_prices:
            row = {
                FILE_HEADERS["A"]: datetime.now(),
                FILE_HEADERS["B"]: i["product_id"],
                FILE_HEADERS["C"]: i["offer_id"],
                FILE_HEADERS["D"]: nomenclatures.get(i["offer_id"], {}).get("Универсальный артикул"),
                FILE_HEADERS["E"]: nomenclatures.get(i["offer_id"], {}).get("Группа"),
                FILE_HEADERS["F"]: nomenclatures.get(i["offer_id"], {}).get("Название товара"),
                FILE_HEADERS["G"]: i["commissions"]["sales_percent_fbo"],
                FILE_HEADERS["H"]: i["commissions"]["sales_percent_fbs"],
                FILE_HEADERS["I"]: "подключены" if i["price"]["auto_action_enabled"] else "нет",
                FILE_HEADERS["J"]: self.str_to_float(i["price"]["old_price"]),
                FILE_HEADERS["K"]: self.str_to_float(i["price"]["price"]),
                FILE_HEADERS["L"]: self.str_to_float(i["price"]["marketing_price"]),
                FILE_HEADERS["M"]: self.str_to_float(i["price"]["marketing_seller_price"]),
                FILE_HEADERS["N"]: self.str_to_float(i["price"]["min_price"]),
                FILE_HEADERS["O"]: self.str_to_float(i["price_index"]),
                FILE_HEADERS["P"]: self.str_to_float(i["price_indexes"]["external_index_data"]["minimal_price"]),
                FILE_HEADERS["Q"]: i["price_indexes"]["external_index_data"]["price_index_value"],
                FILE_HEADERS["R"]: self.str_to_float(i["price_indexes"]["ozon_index_data"]["minimal_price"]),
                FILE_HEADERS["S"]: i["price_indexes"]["ozon_index_data"]["price_index_value"],
                FILE_HEADERS["T"]: self.str_to_float(
                    i["price_indexes"]["self_marketplaces_index_data"]["minimal_price"]
                ),
            }
            result.append(row)
            actions = products_in_all_actions.get(i["product_id"], [])
            for ind, action in enumerate(actions):
                if ind == 0:
                    row.update(
                        {
                            FILE_HEADERS["U"]: "Акции",
                            FILE_HEADERS["V"]: action,
                        }
                    )
                else:
                    result.append({FILE_HEADERS["V"]: action})
        return result
