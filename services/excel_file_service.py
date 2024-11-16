import logging
import string
from datetime import date, datetime, timedelta

import pandas as pd

from extract.nomenclatures import NomenclaturesFile
from extract.ozon_parser import OzonSellerParser
from repositories.product_repository import ProductRepository
from repositories.statistic_repository import StatisticRepository

logger = logging.getLogger(__name__)


class ExcelService:
    company_info = {
        "PRODUCT_CAMPAIGN_MODE_AUTO": "Автоматически",
        "PRODUCT_CAMPAIGN_MODE_MANUAL": "Вручную",
        "MAX_VIEWS": "Максимальное количество показов",
        "MAX_CLICKS": "Максимальное количество кликов для Трафаретов",
        "TOP_MAX_CLICKS": "Максимальное количество кликов для Вывода в топ",
        "NO_AUTO_STRATEGY": "Автостратегия не используется",
        "CAMPAIGN_STATE_RUNNING": "Активная кампания",
        "CAMPAIGN_STATE_PLANNED": "Кампания, сроки проведения которой ещё не наступили",
        "CAMPAIGN_STATE_STOPPED": "Кампания, приостановленная из-за нехватки бюджета",
        "CAMPAIGN_STATE_INACTIVE": "Кампания, остановленная владельцем",
        "CAMPAIGN_STATE_ARCHIVED": "Архивная кампания",
        "CAMPAIGN_STATE_MODERATION_DRAFT": "Отредактированная кампания до отправки на модерацию",
        "CAMPAIGN_STATE_MODERATION_IN_PROGRESS": "Кампания, отправленная на модерацию",
        "CAMPAIGN_STATE_MODERATION_FAILED": "Кампания, непрошедшая модерацию",
        "CAMPAIGN_STATE_FINISHED": "Кампания завершена",
    }

    def __init__(
        self,
        ozon_seller: OzonSellerParser,
        nomenclatures: NomenclaturesFile,
        statistic_repository: StatisticRepository,
        product_repository: ProductRepository,
    ):
        self.ozon_seller = ozon_seller()
        self.nomenclatures = nomenclatures()
        self.statistic_repository = statistic_repository()
        self.product_repository = product_repository()

    @staticmethod
    def str_to_float(str_obj: str) -> float | None:
        """Преобразует строку в тип foat"""
        return float(str_obj.replace(",", ".")) if str_obj else None

    def _products_in_all_actions(self) -> dict:
        """Возвращает словарь где ключ это product_id, а значение - список акций в которых участвует товар"""
        res = {}
        for action in self.ozon_seller.get_actions_list():
            for products in self.ozon_seller.get_list_products_in_actions(action["id"]):
                res.setdefault(products["id"], []).append(action["title"])
        return res

    def _get_trafaret_statistic(self, date_obj: date) -> dict:
        """Возвращает статистику по трафаретам"""
        return {
            record.sku: {
                "campaign_id": record.campaign.campaign_id,
                "product_campaign_mode": record.campaign.product_campaign_mode,
                "product_autopilot_strategy": record.campaign.product_autopilot_strategy,
                "state": record.campaign.state,
                "placement": record.campaign.placement,
                "price": record.price,
                "money_spent": record.money_spent,
                "views": record.views,
                "clicks": record.clicks,
                "ctr": record.ctr,
                "avg_bid": record.avg_bid,
                "orders": record.orders,
                "orders_money": record.orders_money,
                "models": record.models,
                "models_money": record.models_money,
            }
            for record in self.statistic_repository.get_statistics("SKU", date_obj)
        }

    def _get_search_statistic(self, date_obj: date) -> dict:
        """Возвращает статистику по поиску"""
        return {
            record.sku: {
                "campaign_id": record.campaign.campaign_id,
                "product_campaign_mode": record.campaign.product_campaign_mode,
                "product_autopilot_strategy": record.campaign.product_autopilot_strategy,
                "state": record.campaign.state,
                "price": record.price,
                "money_spent": record.money_spent,
                "order_id": record.order_id,
                "order_number": record.order_number,
                "offer_id": record.offer_id,
                "quantity": record.quantity,
                "sale_price": record.sale_price,
                "bid": record.bid,
                "bid_value": record.bid_value,
                "cost": record.cost,
            }
            for record in self.statistic_repository.get_statistics("SEARCH_PROMO", date_obj)
        }

    def _data_for_excel_file(self, date_obj: date):
        """формирование данных для эксель файла"""
        ozone_prices = self.ozon_seller.get_info_price()  # Получаем список с информацией о ценах товара
        nomenclatures = self.nomenclatures.get_nomenclatures()  # Получаем данные из справочника номенклатур
        products_in_all_actions = self._products_in_all_actions()  # Акции в которых участвует товар
        products_ids = {product.external_id: product.sku for product in self.product_repository.get_product()}  # sku
        trafaret_stats = self._get_trafaret_statistic(date_obj)  # Статистика по трафаретам
        search_stats = self._get_search_statistic(date_obj)  # Статистика по поиску

        result = []
        for i in ozone_prices:
            sku = products_ids.get(i["product_id"])
            # ---Добавление цен---
            row = {
                "A": date_obj,
                "B": i["product_id"],
                "C": i["offer_id"],
                "D": nomenclatures.get(i["offer_id"], {}).get("Универсальный артикул"),
                "E": nomenclatures.get(i["offer_id"], {}).get("Группа"),
                "F": nomenclatures.get(i["offer_id"], {}).get("Название товара"),
                "G": i["commissions"]["sales_percent_fbo"],
                "H": i["commissions"]["sales_percent_fbs"],
                "I": "подключены" if i["price"]["auto_action_enabled"] else "нет",
                "J": self.str_to_float(i["price"]["old_price"]),
                "K": self.str_to_float(i["price"]["price"]),
                "L": self.str_to_float(i["price"]["marketing_price"]),
                "M": self.str_to_float(i["price"]["marketing_seller_price"]),
                "N": self.str_to_float(i["price"]["min_price"]),
                "O": self.str_to_float(i["price_index"]),
                "P": self.str_to_float(i["price_indexes"]["external_index_data"]["minimal_price"]),
                "Q": i["price_indexes"]["external_index_data"]["price_index_value"],
                "R": self.str_to_float(i["price_indexes"]["ozon_index_data"]["minimal_price"]),
                "S": i["price_indexes"]["ozon_index_data"]["price_index_value"],
                "T": self.str_to_float(i["price_indexes"]["self_marketplaces_index_data"]["minimal_price"]),
            }
            result.append(row)
            # ---Добавление акций---
            actions = products_in_all_actions.get(i["product_id"], [])
            for action in actions:
                result.append(
                    {
                        "A": date_obj,
                        "B": i["product_id"],
                        "C": i["offer_id"],
                        "D": nomenclatures.get(i["offer_id"], {}).get("Универсальный артикул"),
                        "E": nomenclatures.get(i["offer_id"], {}).get("Группа"),
                        "F": nomenclatures.get(i["offer_id"], {}).get("Название товара"),
                        "U": "Акции",
                        "V": action,
                    }
                )
            # ---Добавление статистики по трафоретам---
            trafaret_stat = trafaret_stats.get(sku)
            if trafaret_stat:
                trafaret_values = {
                    "A": date_obj,
                    "B": i["product_id"],
                    "C": i["offer_id"],
                    "D": nomenclatures.get(i["offer_id"], {}).get("Универсальный артикул"),
                    "E": nomenclatures.get(i["offer_id"], {}).get("Группа"),
                    "F": nomenclatures.get(i["offer_id"], {}).get("Название товара"),
                    "U": "Вывод в ТОП" if trafaret_stat.get("placement") == "PLACEMENT_TOP_PROMOTION" else "Трафареты",
                    "V": f'№ {trafaret_stat.get("campaign_id")}',
                    "W": self.company_info.get(trafaret_stat.get("product_campaign_mode")),
                    "X": self.company_info.get(trafaret_stat.get("product_autopilot_strategy")),
                    "Y": self.company_info.get(trafaret_stat.get("state")),
                    "AA": trafaret_stat.get("views"),
                    "AB": trafaret_stat.get("clicks"),
                    "AC": trafaret_stat.get("ctr"),
                    "AE": trafaret_stat.get("avg_bid"),
                    "AF": trafaret_stat.get("money_spent"),
                    "AG": trafaret_stat.get("orders"),
                    "AH": trafaret_stat.get("orders_money"),
                    "AI": trafaret_stat.get("models"),
                    "AJ": trafaret_stat.get("models_money"),
                }
                result.append(trafaret_values)
            # ---Добавление статистики по поиску---
            search_stat = search_stats.get(sku)
            if search_stat:
                search_values = {
                    "A": date_obj,
                    "B": i["product_id"],
                    "C": i["offer_id"],
                    "D": nomenclatures.get(i["offer_id"], {}).get("Универсальный артикул"),
                    "E": nomenclatures.get(i["offer_id"], {}).get("Группа"),
                    "F": nomenclatures.get(i["offer_id"], {}).get("Название товара"),
                    "U": "Продвижение в поиске",
                    "V": f'№ {search_stat.get("campaign_id")}',
                    "W": self.company_info.get(trafaret_stat.get("product_campaign_mode")),
                    "X": self.company_info.get(trafaret_stat.get("product_autopilot_strategy")),
                    "Y": self.company_info.get(trafaret_stat.get("state")),
                    "AE": search_stat.get("bid_value"),
                    "AF": search_stat.get("money_spent"),
                    "AG": search_stat.get("quantity"),
                    "AH": search_stat.get("cost"),
                    "AK": search_stat.get("bid"),
                    "AM": search_stat.get("order_id"),
                    "AN": search_stat.get("order_number"),
                }
                result.append(search_values)
        return result

    def load_data(self, date_obj: date | str = (datetime.now() - timedelta(days=1)).date()):
        """Дозаписывает данные в файл"""
        if isinstance(date_obj, str):
            date_obj = datetime.strptime(date_obj, "%Y-%m-%d").date()
        data = self._data_for_excel_file(date_obj)
        file_path = "Общая модель.xlsx"

        uppercase_letters = list(string.ascii_uppercase)
        uppercase_letters.extend([uppercase_letters[0] + i for i in uppercase_letters])
        uppercase_letters.extend(["BA"])

        df_new = pd.DataFrame(data, columns=uppercase_letters)

        with pd.ExcelWriter(file_path, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
            df_new.to_excel(
                writer,
                index=False,
                header=False,
                sheet_name="Содержательная бизнес логика",
                startrow=writer.sheets["Содержательная бизнес логика"].max_row,
            )
            logger.info("Данные успешно добавлены в файл.")
