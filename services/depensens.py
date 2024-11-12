from extract.nomenclatures import NomenclaturesFile
from extract.ozon_parser import OzonPerformanceParser, OzonSellerParser
from repositories.campaign_repository import CampaignRepository
from repositories.statistic_repository import StatisticRepository
from repositories.token_repository import TokenRepository
from services.campaign_service import CampaignService
from services.excel_file_service import ExcelService
from services.statistic_service import StatisticService


def campaign_service():
    return CampaignService(OzonPerformanceParser, CampaignRepository, TokenRepository)


def excel_service():
    return ExcelService(OzonSellerParser, NomenclaturesFile)


def statistic_service():
    return StatisticService(OzonPerformanceParser, CampaignRepository, StatisticRepository, TokenRepository)
