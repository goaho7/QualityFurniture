import logging
import time
from itertools import islice

from extract.ozon_parser import OzonPerformanceParser
from repositories.campaign_repository import CampaignRepository
from repositories.statistic_repository import StatisticRepository
from repositories.token_repository import TokenRepository

logging.basicConfig(
    level=logging.DEBUG, format="%(filename)s:%(lineno)d #%(levelname)-8s " "[%(asctime)s] - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)


class StatisticService:
    def __init__(
        self,
        ozon_performance: OzonPerformanceParser,
        campaign_repository: CampaignRepository,
        statistic_repository: StatisticRepository,
        token_repository: TokenRepository,
    ):
        self.ozon_performance = ozon_performance(token_repository)
        self.campaign_repository = campaign_repository()
        self.statistic_repository = statistic_repository()

    def all_reports(self) -> list:
        """Сохранить все отчёты за вчерашнюю дату"""
        start = time.perf_counter()

        campaigns = self.campaign_repository.get_campaigns()  # Получение списка кампаний
        campaign_id_list = [i.campaign_id for i in campaigns]  # Список ID кампаний
        campaign_id_dict = {i.campaign_id: i.id for i in campaigns}

        def chunks(iterable, size=10):
            """Выдаёт по 10 элементов за раз у итерируемого объекта 'iterable'"""
            iterator = iter(iterable)
            while chunk := list(islice(iterator, size)):
                yield chunk

        for chunk_id_list in chunks(campaign_id_list):  # Цикл на получение по 10 кампаний в отчёте
            uuid = self.ozon_performance.campaign_statistics(chunk_id_list)  # Запрос на создание отчёта

            while True:
                time.sleep(3)
                check_status = self.ozon_performance.check_report_result(uuid)  # Проверка статуса отчёта
                if check_status == "OK":
                    logger.info(f"Статус 'OK', получаем отчёт: {uuid}")
                    reports = self.ozon_performance.get_reports(uuid)  # Получение отчёта
                    logger.info(f"Сохраняем отчёт: {uuid}")
                    self.statistic_repository.update_statistics(reports, campaign_id_dict)  # Сохранение отчёта в БД
                    logger.info(f"Отчёт: {uuid} сохранён")
                    break
                logger.info(f"Статус отчёта {uuid}: {check_status} ждём 30 сек")
                time.sleep(30)
        work_time = time.perf_counter() - start
        logger.info(f"Отчёты загружены, время выполнения: {round(work_time, 4)} сек.")
