import logging
from datetime import datetime, timedelta

import pandas as pd
import requests

from extract.ozon_parser import OzonPerformanceParser, OzonSellerParser
from repositories.campaign_repository import CampaignRepository
from repositories.product_repository import ProductRepository
from repositories.statistic_repository import StatisticRepository
from repositories.token_repository import TokenRepository
from services.depensens import (
    campaign_service,
    excel_service,
    product_service,
    statistic_service,
)

logging.basicConfig(
    level=logging.INFO, format="%(filename)s:%(lineno)d #%(levelname)-4s " "[%(asctime)s] - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # campaign_service().update_campaigns()
    # product_service().update_products()
    # statistic_service().all_reports_load()
    # d = (datetime.now() - timedelta(days=1)).date()
    excel_service().load_data()
