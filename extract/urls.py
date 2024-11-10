class OzonSellerUrls:
    price_info = "https://api-seller.ozon.ru/v4/product/info/prices"  # Получить информацию о цене товара
    actions = "https://api-seller.ozon.ru/v1/actions"  # Список акций
    list_products_in_actions = "https://api-seller.ozon.ru/v1/actions/products"  # Список участвующих в акции товаров
    list_products_available_in_actions = (
        "https://api-seller.ozon.ru/v1/actions/candidates"  # Список доступных для акции товаров
    )


class OzonPerformanceUrls:
    campaigns = "https://api-performance.ozon.ru:443/api/client/campaign"  # Список кампаний
    statistics = "https://api-performance.ozon.ru:443/api/client/statistics/json"  # Запросить статистику по кампании в формате JSON
    check_report_result = "https://api-performance.ozon.ru:443/api/client/statistics/"  # +{UUID} Cтатус отчёта
    get_reports = "https://api-performance.ozon.ru:443/api/client/statistics/report"  # Получить отчёты
    get_access_token = "https://api-performance.ozon.ru/api/client/token"  # Получить токен
