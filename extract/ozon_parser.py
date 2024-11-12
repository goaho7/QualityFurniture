import logging
import os
import time
from datetime import datetime

import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException

from extract.urls import OzonPerformanceUrls, OzonSellerUrls
from settings import REQUESTS_SESSION

logging.basicConfig(
    level=logging.INFO, format="%(filename)s:%(lineno)d #%(levelname)-8s " "[%(asctime)s] - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

load_dotenv()


class OzonSellerParser:
    """Данные с Ozon Seller"""

    __HEADERS = {"Client-Id": os.getenv("client_id"), "Api-Key": os.getenv("client_secret")}

    def __init__(self):
        self.session = REQUESTS_SESSION

    def _make_request(self, method, url, session=True, **kwargs):
        """Создаёт запрос, при неудаче пробует ещё 2 раза чезе 3 сек."""
        request = self.session if session else requests
        for _ in range(3):
            try:
                response = request.request(method, url, **kwargs)
                if response.status_code == 404:
                    return None
                response.raise_for_status()
                return response.json()
            except RequestException as e:
                logger.error(f"Ошибка при запросе {url}: {e}")
                time.sleep(3)
        return None

    def get_info_price(self) -> list:
        """Получить список с информацией о цене товара"""
        payload = {"filter": {}, "last_id": "", "limit": 100}
        response = self._make_request("post", OzonSellerUrls.price_info, headers=self.__HEADERS, json=payload)

        data = response.get("result", {}).get("items", [])
        if len(data) == response["result"]["total"]:
            return data
        result = []
        result.extend(data)
        while response:
            payload.update({"last_id": response["result"]["last_id"]})
            response = self._make_request("post", OzonSellerUrls.price_info, headers=self.__HEADERS, json=payload)
            if response is None:
                break
            result.extend(response["result"]["items"])
        return result

    def get_actions_list(self) -> list:
        """Получить список акций"""
        try:
            response = self.session.get(OzonSellerUrls.actions, headers=self.__HEADERS)
            response.raise_for_status()
            return response.json()["result"]
        except RequestException as e:
            logger.error(f"Ошибка при получении списка акций: {e}")
            return None

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
            for _ in range(3):
                try:
                    response = self.session.post(url, headers=self.__HEADERS, json=payload)
                    response.raise_for_status()
                    data = response.json()
                    break
                except RequestException as e:
                    logger.error(f"Ошибка при получении списка товаров для акций: {e}")
                    time.sleep(3)
            products.extend(data["result"]["products"])
            offset += limit
            total = data["result"]["total"]
            if offset >= total:
                break
        return products


class OzonPerformanceParser:
    """Данные с Ozon Performance"""

    def __init__(self, token_repository):
        self.session = REQUESTS_SESSION
        self.token_repository = token_repository()
        self.timeout = 30
        self._headers = {"Authorization": f"Bearer {self.get_access_token()}"}

    def _make_request(self, method, url, session=True, **kwargs):
        """Создаёт запрос, при неудаче пробует ещё 2 раза чезе 5 сек."""
        request = self.session if session else requests
        for _ in range(3):
            try:
                response = request.request(method, url, timeout=self.timeout, **kwargs)
                response.raise_for_status()
                return response.json()
            except RequestException as e:
                if response and response.status_code == 404:
                    return None
                if response and response.status_code == 403:
                    self.update_access_token()
                logger.error(f"Ошибка при запросе {url}: {e}")
                time.sleep(5)
        return None

    def update_access_token(self):
        """Обновить токен в БД"""
        payload = {
            "client_id": os.getenv("client_id_performance"),
            "client_secret": os.getenv("client_secret_performance"),
            "grant_type": "client_credentials",
        }
        response = self._make_request("post", OzonPerformanceUrls.get_access_token, json=payload)
        if response is None:
            raise RequestException("Не удалось получить новый токен после нескольких попыток.")
        access_token = response["access_token"]
        self.token_repository.update_token(access_token)
        logger.info("Токен обновлён")

    def get_access_token(self):
        """Получение access токена из БД (если нет, или истёк - обновляется)"""
        token = self.token_repository.get_token()
        if not token or int(time.time()) - token.created_at >= token.expires_in - 100:
            self.update_access_token()
            token = self.token_repository.get_token()
        return token.access_token

    def get_campaign_list(self) -> list:
        """Получить список кампаний"""
        response = self._make_request("get", OzonPerformanceUrls.campaigns, headers=self._headers)
        if response is None:
            raise RequestException("Не удалось получить список кампаний после нескольких попыток.")
        return response["list"]

    def campaign_statistics(self, campaign_id_list, date: datetime) -> str:
        """Сделать запрос и получить UUID запроса на статистику по кампаниям (максимум 10 кампаний за раз)"""
        yesterday_str = date.strftime("%Y-%m-%d")
        payload = {
            "campaigns": campaign_id_list,
            "dateFrom": yesterday_str,
            "dateTo": yesterday_str,
        }
        response = self._make_request("post", OzonPerformanceUrls.statistics, headers=self._headers, json=payload)
        if response is None:
            raise RequestException("Не удалось сделать запрос на статистику по кампаниям после нескольких попыток.")
        return response["UUID"]

    def check_report_result(self, uuid) -> str:
        """
        Проверка статуса запроса:
        NOT_STARTED — запрос ожидает выполнения;
        IN_PROGRESS — запрос выполняется в данный момент;
        ERROR — выполнение запроса завершилось ошибкой;
        OK — запрос успешно выполнен.
        """
        response = self._make_request(
            "get", OzonPerformanceUrls.check_report_result + uuid, session=False, headers=self._headers
        )
        if response is None:
            raise RequestException("Не удалось сделать запрос на проверку статуса запроса после нескольких попыток.")
        return response["state"]

    def get_reports(self, uuid: str) -> dict:
        """Получить отчёты по UUID"""
        response = self._make_request(
            "get", OzonPerformanceUrls.get_reports, headers=self._headers, params={"UUID": uuid}
        )
        if response is None:
            raise RequestException("Не удалось получить отчёты по UUID после нескольких попыток.")
        return response
