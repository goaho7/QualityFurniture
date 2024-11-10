from datetime import datetime

from models.models import Campaign, sqlite_session


class CampaignRepository:
    model = Campaign

    def get_campaigns(self, state: str = None, adv_object_type: str = None):
        """Получить все кампании с фильтрацией по полям state и advObjectType"""
        with sqlite_session() as session:
            query = session.query(self.model)
            if state:
                query = query.filter(self.model.state == state)
            if adv_object_type:
                query = query.filter(self.model.adv_object_type == adv_object_type)
            return query.all()

    def update_campaign(self, data: list):
        """Обновление таблицы кампаний"""
        with sqlite_session() as session:
            session.query(self.model).delete()
            campaigns = []
            for c in data:
                campaign = self.model(
                    campaign_id=c["id"],
                    title=c["title"],
                    state=c["state"],
                    adv_object_type=c["advObjectType"],
                    from_date=datetime.fromisoformat(c["fromDate"]) if c["fromDate"] else None,
                    to_date=datetime.fromisoformat(c["toDate"]) if c["toDate"] else None,
                    budget=float(c["budget"]),
                    daily_budget=float(c["dailyBudget"]),
                    weekly_budget=float(c["weeklyBudget"]),
                    placement=", ".join(c["placement"]),
                    product_autopilot_strategy=c["productAutopilotStrategy"],
                    product_campaign_mode=c["productCampaignMode"],
                )
                campaigns.append(campaign)
            session.bulk_save_objects(campaigns)
            session.commit()
