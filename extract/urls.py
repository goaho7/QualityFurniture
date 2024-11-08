OZON_SELLER_HOST = "https://api-seller.ozon.ru/"
OZON_PERFORMANCE_HOST = "https://api-performance.ozon.ru:443/api/client/"


class OzonSellerUrls:
    price_info = OZON_SELLER_HOST + "v4/product/info/prices"  # Получить информацию о цене товара
    actions = OZON_SELLER_HOST + "v1/actions"  # Список акций
    list_products_in_actions = OZON_SELLER_HOST + "v1/actions/products"  # Список участвующих в акции товаров
    list_products_available_in_actions = (
        OZON_SELLER_HOST + "v1/actions/candidates"
    )  # Список доступных для акции товаров


class OzonPerformanceUrls:
    statistics = OZON_PERFORMANCE_HOST + "statistics/json"  # Статистика по кампании в формате JSON
