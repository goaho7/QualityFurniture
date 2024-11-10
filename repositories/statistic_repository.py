from datetime import datetime, timedelta

from models.models import CampaignStatistics, sqlite_session


class StatisticRepository:
    model = CampaignStatistics

    def update_statistics(self, data: dict, campaigns: dict):
        """Обновить таблицу статистики"""
        with sqlite_session() as session:
            statistics = []
            for key, value in data.items():
                if value["report"]["rows"]:
                    for i in value["report"]["rows"]:
                        statistic = self.model(
                            date=(datetime.now() - timedelta(days=1)),
                            product_name=i.get("title"),
                            sku=i.get("sku"),
                            views=i.get("views"),
                            ctr=float(i.get("ctr").replace(",", ".")) if i.get("ctr") else None,
                            clicks=i.get("clicks"),
                            conversion=None,
                            avg_bid=float(i.get("avgBid").replace(",", ".")) if i.get("avgBid") else None,
                            money_spent=float(i.get("moneySpent").replace(",", ".")) if i.get("moneySpent") else None,
                            orders=i.get("orders"),
                            orders_money=(
                                float(i.get("ordersMoney").replace(",", ".")) if i.get("ordersMoney") else None
                            ),
                            models=i.get("models"),
                            models_money=(
                                float(i.get("modelsMoney").replace(",", ".")) if i.get("modelsMoney") else None
                            ),
                            reach=None,
                            order_id=None,
                            order_number=None,
                            ozon_id=None,
                            ozon_id_of_promoted_product=None,
                            article=None,
                            name=None,
                            quantity=None,
                            price=float(i.get("price").replace(",", ".")) if i.get("price") else None,
                            cost=None,
                            bid_in_percent=None,
                            bid=None,
                            banner=None,
                            banner_id=None,
                            page_type=i.get("pageType"),
                            display_condition=None,
                            platform=None,
                            avg_price_per_1000_impressions=None,
                            iab_viewable_impressions=None,
                            share_viewable_impressions=None,
                            inspections_quartiles_25=None,
                            inspections_quartiles_50=None,
                            inspections_quartiles_75=None,
                            inspections_quartiles_100=None,
                            share_inspections_25=None,
                            share_inspections_50=None,
                            share_inspections_75=None,
                            share_inspections_100=None,
                            views_with_sound=None,
                            campaign_id=campaigns[int(key)],
                        )
                        statistics.append(statistic)
            session.bulk_save_objects(statistics)
            session.commit()
