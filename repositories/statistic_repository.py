from datetime import datetime

from sqlalchemy.dialects.sqlite import insert

from models import (
    BannerStatistics,
    SearchStatistics,
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

    def update_statistics(self, data: dict, campaigns: dict, date: datetime):
        """Обновить таблицы статистики"""

        with sqlite_session() as session:
            for key, value in data.items():
                if value["report"]["rows"]:
                    for i in value["report"]["rows"]:
                        model = self.model.get(campaigns[int(key)][1])
                        if model:
                            index_elements = self.index_elements[campaigns[int(key)][1]]
                            insert_values = {
                                "campaign_id": campaigns[int(key)][0],
                                "date": date,
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
                                        "reach": i.get("reach"),
                                        "orders": i.get("orders"),
                                        "order_id": i.get("order_id"),
                                        "order_number": i.get("order_number"),
                                        "adv_sku": i.get("adv_sku"),
                                        "offer_id": i.get("offer_id"),
                                        "quantity": i.get("quantity"),
                                        "sale_price": self.str_to_float(i.get("sale_price")),
                                        "bid": self.str_to_float(i.get("bid")),
                                        "bid_value": self.str_to_float(i.get("bid_value")),
                                        "orders_money": self.str_to_float(i.get("ordersMoney")),
                                        "models": i.get("models"),
                                        "models_money": self.str_to_float(i.get("modelsMoney")),
                                        "banner": i.get("banner"),
                                        "page_type": i.get("pageType"),
                                        "attributes_platform": i.get("attributes_platform"),
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
