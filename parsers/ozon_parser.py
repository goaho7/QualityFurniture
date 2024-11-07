import os

from dotenv import load_dotenv

from parsers.urls import OzonPerformanceUrls, OzonSellerUrls
from settings import REQUESTS_SESSION

load_dotenv()


class OzonSellerParser:

    __HEADERS = {"Client-Id": os.getenv("client_id"), "Api-Key": os.getenv("client_secret")}

    def __init__(self):
        self.session = REQUESTS_SESSION

    def get_info_price(self) -> list:
        """Получить список с информацией о цене товара"""
        payload = {"filter": {}, "last_id": "", "limit": 1000}
        response = self.session.post(OzonSellerUrls.price_info, headers=self.__HEADERS, json=payload)
        result = []
        if response.status_code == 200:
            data = response.json()
            result.extend(data["result"]["items"])
            if len(result) == data["result"]["total"]:
                return result
            while True:
                payload.update({"last_id": data["result"]["last_id"]})
                response = self.session.post(OzonSellerUrls.price_info, headers=self.__HEADERS, json=payload)
                if response.status_code != 200:
                    break
                data = response.json()
                result.extend(data["result"]["items"])
            return result
        print(response.status_code)

    def get_actions_list(self) -> list:
        """Получить список акций"""
        response = self.session.get(OzonSellerUrls.actions, headers=self.__HEADERS)
        if response.status_code == 200:
            return response.json()["result"]
        print(response.status_code)

    def get_list_products_in_actions(self, action_id, is_participates=True) -> list:
        """
        Если is_participates=True метод возвращает список участвующих в акции товаров,
        если is_participates=False список доступных для акции товаров
        """
        url = (
            OzonSellerUrls.list_products_in_actions
            if is_participates
            else OzonSellerUrls.list_products_available_in_actions
        )
        products = []
        offset = 0
        limit = 1000
        while True:
            payload = {"action_id": action_id, "limit": limit, "offset": offset}
            response = self.session.post(url, headers=self.__HEADERS, json=payload)
            if response.status_code != 200:
                print(response.status_code)
                return
            data = response.json()
            products.extend(data["result"]["products"])
            offset += limit
            total = data["result"]["total"]
            if offset >= total:
                break
        return products


class OzonPerformanceParser:
    pass
