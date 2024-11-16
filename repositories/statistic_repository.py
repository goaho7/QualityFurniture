from datetime import date, datetime

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import joinedload

from models import (
    BannerStatistics,
    SearchStatistics,
    StatisticsHistory,
    StencilStatistics,
    VideoBannerStatistics,
    sqlite_session,
)


class StatisticRepository:
    model = {
        "BANNER": BannerStatistics,
        "SEARCH_PROMO": SearchStatistics,
        "SKU": StencilStatistics,
        "VIDEO_BANNER": VideoBannerStatistics,
        "STAT_HISTORY": StatisticsHistory,
    }
    index_elements = {
        "BANNER": ["campaign_id", "date"],
        "SEARCH_PROMO": ["date", "sku"],
        "SKU": ["date", "sku"],
        "VIDEO_BANNER": ["campaign_id", "date"],
    }

    @staticmethod
    def str_to_float(string: str):
        """Преобразует строку в тип foat"""
        return float(string.replace(",", ".")) if string else None

    def get_statistics(self, type_campaign: str, date_obj: date | str):
        """Получить статистику по типу кампании и дате"""
        if isinstance(date_obj, str):
            date_obj = datetime.strptime(date_obj, "%Y-%m-%d").date()
        with sqlite_session() as session:
            model = self.model.get(type_campaign)
            if model is None:
                raise ValueError(f"Неизвестный тип кампании: {type_campaign}")
            query = session.query(model).filter(model.date == date_obj).options(joinedload(model.campaign))
            return query.all()

    def update_statistics(self, data: dict, campaigns: dict, date_obj: datetime | str):
        """Обновить таблицы статистики"""
        if isinstance(date_obj, str):
            date_obj = datetime.strptime(date_obj, "%Y-%m-%d").date()
        with sqlite_session() as session:
            for key, value in data.items():
                if value["report"]["rows"]:
                    for i in value["report"]["rows"]:
                        model = self.model.get(campaigns[int(key)][1])
                        if model:
                            index_elements = self.index_elements[campaigns[int(key)][1]]
                            insert_values = {
                                "campaign_id": campaigns[int(key)][0],
                                "date": date_obj,
                                **{
                                    field: value
                                    for field, value in {
                                        "sku": i.get("sku"),
                                        "name": i.get("title"),
                                        "price": self.str_to_float(i.get("price")),
                                        "money_spent": self.str_to_float(i.get("moneySpent")),
                                        "views": i.get("views"),
                                        "clicks": i.get("clicks"),
                                        "ctr": self.str_to_float(i.get("ctr")),
                                        "avg_bid": self.str_to_float(i.get("avgBid")),
                                        "reach": self.str_to_float(i.get("reach")),
                                        "orders": i.get("orders"),
                                        "order_id": i.get("orderId"),
                                        "order_number": i.get("orderNumber"),
                                        "adv_sku": i.get("advSku"),
                                        "offer_id": i.get("offerId"),
                                        "quantity": i.get("quantity"),
                                        "sale_price": self.str_to_float(i.get("salePrice")),
                                        "bid": self.str_to_float(i.get("bid")),
                                        "bid_value": self.str_to_float(i.get("bidValue")),
                                        "orders_money": self.str_to_float(i.get("ordersMoney")),
                                        "models": i.get("models"),
                                        "models_money": self.str_to_float(i.get("modelsMoney")),
                                        "banner": i.get("banner"),
                                        "page_type": i.get("pageType"),
                                        "attributes_platform": i.get("attributesPlatform"),
                                        "cost": self.str_to_float(i.get("cost")),
                                    }.items()
                                    if hasattr(model, field)
                                },
                            }
                            insert_stmt = insert(model).values(insert_values)

                            update_values = {
                                field: value
                                for field, value in insert_values.items()
                                if field in model.__table__.columns
                            }
                            on_conflict_stmt = insert_stmt.on_conflict_do_update(
                                index_elements=index_elements,
                                set_=update_values,
                            )
                            session.execute(on_conflict_stmt)
            session.commit()

    def get_record_by_date(self, date_obj: date):
        """Получение записи с uuids отчётов за дату"""
        model = self.model["STAT_HISTORY"]
        with sqlite_session() as session:
            return session.query(model).filter(model.date == date_obj).one_or_none()

    def update_statistics_history(self, data: dict):
        """Добавить/обновить историю загруженных отчётов"""
        with sqlite_session() as session:
            insert_stmt = insert(self.model["STAT_HISTORY"]).values(
                date=data["date"],
                uuids=data["uuids"],
            )
            on_conflict_stmt = insert_stmt.on_conflict_do_update(
                index_elements=["date"],
                set_={
                    "date": data["date"],
                    "uuids": data["uuids"],
                },
            )
            session.execute(on_conflict_stmt)
            session.commit()
