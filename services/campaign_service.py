import logging

from extract.ozon_parser import OzonPerformanceParser
from repositories.campaign_repository import CampaignRepository
from repositories.token_repository import TokenRepository

logger = logging.getLogger(__name__)


class CampaignService:
    def __init__(
        self,
        ozon_performance: OzonPerformanceParser,
        campaign_repository: CampaignRepository,
        token_repository: TokenRepository,
    ):
        self.ozon_performance = ozon_performance(token_repository)
        self.campaign_repository = campaign_repository()

    def update_campaigns(self):
        """Обновить таблицу кампаний в БД"""
        data = self.ozon_performance.get_campaign_list()  # Получение кампаний через API
        self.campaign_repository.update_campaign(data)  # Сохранение в БД
        logger.info("Кампании обновлены")
