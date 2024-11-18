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
    date = (datetime.now() - timedelta(days=1)).date()
    # campaign_service().update_campaigns()
    # product_service().update_products()
    statistic_service().all_reports_load("2024-11-16")
    # excel_service().load_data("2024-11-17")
