from settings import FILE_HEADERS


class PriceTransform:
    def transform_ozone(self, data_price: list, nomenclatures: dict):
        return [
            {
                FILE_HEADERS["B"]: i["product_id"],
                FILE_HEADERS["C"]: i["offer_id"],
                FILE_HEADERS["D"]: nomenclatures.get(i["offer_id"], {}).get("Универсальный артикул"),
                FILE_HEADERS["E"]: nomenclatures.get(i["offer_id"], {}).get("Группа"),
                FILE_HEADERS["F"]: nomenclatures.get(i["offer_id"], {}).get("Название товара"),
                FILE_HEADERS["G"]: i["commissions"]["sales_percent_fbo"],
                FILE_HEADERS["H"]: i["commissions"]["sales_percent_fbs"],
                FILE_HEADERS["I"]: "подключены" if i["price"]["auto_action_enabled"] else "нет",
                FILE_HEADERS["J"]: i["price"]["old_price"],
                FILE_HEADERS["K"]: i["price"]["price"],
                FILE_HEADERS["L"]: i["price"]["marketing_price"],
                FILE_HEADERS["M"]: i["price"]["marketing_seller_price"],
                FILE_HEADERS["N"]: i["price"]["min_price"],
                FILE_HEADERS["O"]: i["price_index"],
                FILE_HEADERS["P"]: i["price_indexes"]["external_index_data"]["minimal_price"],
                FILE_HEADERS["Q"]: i["price_indexes"]["external_index_data"]["price_index_value"],
                FILE_HEADERS["R"]: i["price_indexes"]["ozon_index_data"]["minimal_price"],
                FILE_HEADERS["S"]: i["price_indexes"]["ozon_index_data"]["price_index_value"],
                FILE_HEADERS["T"]: i["price_indexes"]["self_marketplaces_index_data"]["minimal_price"],
            }
            for i in data_price
        ]
