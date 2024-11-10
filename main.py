import pandas as pd

from extract.nomenclatures import NomenclaturesFile
from extract.ozon_parser import OzonPerformanceParser, OzonSellerParser
from repositories.campaign_repository import CampaignRepository
from repositories.statistic_repository import StatisticRepository
from repositories.token_repository import TokenRepository
from services.campaign_service import CampaignService
from services.price_service import PriceService
from services.statistic_service import StatisticService
from transforms.price_transforms import PriceTransform


def load_price_data():
    data = PriceService(OzonSellerParser, NomenclaturesFile, PriceTransform).data()
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

        print("Данные успешно добавлены.")


if __name__ == "__main__":
    statistic_service = StatisticService(
        OzonPerformanceParser, CampaignRepository, StatisticRepository, TokenRepository
    )
    campaign_service = CampaignService(OzonPerformanceParser, CampaignRepository, TokenRepository)

    campaign_service.update_campaigns()
    statistic_service.all_reports()
