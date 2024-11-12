import logging

import pandas as pd
import requests

from extract.ozon_parser import OzonPerformanceParser, OzonSellerParser
from repositories.campaign_repository import CampaignRepository
from repositories.token_repository import TokenRepository
from services.depensens import campaign_service, excel_service, statistic_service

logging.basicConfig(
    level=logging.DEBUG, format="%(filename)s:%(lineno)d #%(levelname)-8s " "[%(asctime)s] - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)


def load_data(data: dict):
    """Дозаписывает данные в файл"""
    file_path = "Общая модель.xlsx"

    df_new = pd.DataFrame(data)

    with pd.ExcelWriter(file_path, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
        df_new.to_excel(
            writer,
            index=False,
            header=False,
            sheet_name="Содержательная бизнес логика",
            startrow=writer.sheets["Содержательная бизнес логика"].max_row,
        )
        logger.info("Данные успешно добавлены в файл.")


if __name__ == "__main__":
    # campaign_service().update_campaigns()
    # statistic_service().all_reports()

    # for i, j in excel_service().products_in_all_actions().items():
    #     print(i, j)
    load_data(excel_service().prices())
