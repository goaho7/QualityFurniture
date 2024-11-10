import time

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker

BaseModel = declarative_base()


class Base(BaseModel):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


class Token(Base):
    """Токен"""

    __tablename__ = "token"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    access_token: Mapped[str] = mapped_column(String(1500), unique=True)
    created_at: Mapped[int] = mapped_column(Integer, default=lambda: int(time.time()))
    expires_in: Mapped[int] = mapped_column(Integer, default=1800)


class Campaign(Base):
    """Кампании"""

    __tablename__ = "campaign"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(comment="ID кампании")
    title: Mapped[str] = mapped_column(String(255), comment="Название кампании")
    state: Mapped[str] = mapped_column(String(255), comment="Состояние кампании")
    adv_object_type: Mapped[str] = mapped_column(String(255), comment="Тип рекламируемой кампании")
    from_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True, comment="Дата старта рекламной кампании")
    to_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True, comment="Дата завершения рекламной кампании")
    budget: Mapped[float] = mapped_column(nullable=True, comment="Бюджет рекламной кампании")
    daily_budget: Mapped[float] = mapped_column(nullable=True, comment="Дневной бюджет рекламной кампани")
    weekly_budget: Mapped[float] = mapped_column(nullable=True, comment="Недельный бюджет рекламной кампани")
    placement: Mapped[str] = mapped_column(String(255), nullable=True, comment="Место размещения рекламы")
    product_autopilot_strategy: Mapped[str] = mapped_column(
        String(255), comment="Автостратегия, которая используется для кампании"
    )
    product_campaign_mode: Mapped[str] = mapped_column(
        String(255), comment="Режим создания и управления товарной рекламной кампанией"
    )

    campaign_statistics: Mapped[list["CampaignStatistics"]] = relationship(
        "CampaignStatistics", back_populates="campaign"
    )


class CampaignStatistics(Base):
    """Статистика по всем кампаниям"""

    __tablename__ = "campaign_statistics"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaign.id"), comment="ID кампании")
    date: Mapped[Date] = mapped_column(Date)
    product_name: Mapped[str] = mapped_column(String(255), nullable=True, comment="Название товара")
    sku: Mapped[str] = mapped_column(String(255), nullable=True, comment="SKU")
    views: Mapped[int] = mapped_column(nullable=True, comment="Показы")
    ctr: Mapped[float] = mapped_column(nullable=True, comment="CTR (%)")
    clicks: Mapped[int] = mapped_column(nullable=True, comment="Клики")
    conversion: Mapped[float] = mapped_column(nullable=True, comment="Конверсия")
    avg_bid: Mapped[float] = mapped_column(nullable=True, comment="Ср. цена клика, руб")
    money_spent: Mapped[float] = mapped_column(nullable=True, comment="Расход, руб, с НДС")
    orders: Mapped[int] = mapped_column(nullable=True, comment="Заказы")
    orders_money: Mapped[float] = mapped_column(nullable=True, comment="Выручка")
    models: Mapped[int] = mapped_column(nullable=True, comment="Заказы модели")
    models_money: Mapped[float] = mapped_column(nullable=True, comment="Выручка с заказов модели")
    reach: Mapped[float] = mapped_column(nullable=True, comment="Охват")
    order_id: Mapped[int] = mapped_column(nullable=True, comment="ID заказа")
    order_number: Mapped[int] = mapped_column(nullable=True, comment="Номер заказа")
    ozon_id: Mapped[int] = mapped_column(nullable=True, comment="Ozon ID")
    ozon_id_of_promoted_product: Mapped[int] = mapped_column(nullable=True, comment="Ozon ID продвигаемого товара")
    article: Mapped[str] = mapped_column(String(255), nullable=True, comment="Артикул")
    name: Mapped[str] = mapped_column(String(255), nullable=True, comment="Наименование")
    quantity: Mapped[int] = mapped_column(nullable=True, comment="Количество")
    price: Mapped[float] = mapped_column(nullable=True, comment="Цена продажи")
    cost: Mapped[float] = mapped_column(nullable=True, comment="Стоимость")
    bid_in_percent: Mapped[float] = mapped_column(nullable=True, comment="Ставка в процентах")
    bid: Mapped[float] = mapped_column(nullable=True, comment="Ставка")
    banner: Mapped[str] = mapped_column(String(255), nullable=True, comment="Баннер")
    banner_id: Mapped[int] = mapped_column(nullable=True, comment="ID баннера")
    page_type: Mapped[str] = mapped_column(String(255), nullable=True, comment="Тип страницы")
    display_condition: Mapped[str] = mapped_column(String(255), nullable=True, comment="Условие показа")
    platform: Mapped[str] = mapped_column(String(255), nullable=True, comment="Платформа")
    avg_price_per_1000_impressions: Mapped[float] = mapped_column(nullable=True, comment="Ср. цена 1000 показов")
    iab_viewable_impressions: Mapped[int] = mapped_column(nullable=True, comment="Видимые показы IAB")
    share_viewable_impressions: Mapped[float] = mapped_column(nullable=True, comment="Доля видимых показов")
    inspections_quartiles_25: Mapped[float] = mapped_column(nullable=True, comment="Досмотры по квартилям 25%")
    inspections_quartiles_50: Mapped[float] = mapped_column(nullable=True, comment="Досмотры по квартилям 50%")
    inspections_quartiles_75: Mapped[float] = mapped_column(nullable=True, comment="Досмотры по квартилям 75%")
    inspections_quartiles_100: Mapped[float] = mapped_column(nullable=True, comment="Досмотры по квартилям 100%")
    share_inspections_25: Mapped[float] = mapped_column(nullable=True, comment="Доля досмотров 25%")
    share_inspections_50: Mapped[float] = mapped_column(nullable=True, comment="Доля досмотров 50%")
    share_inspections_75: Mapped[float] = mapped_column(nullable=True, comment="Доля досмотров 75%")
    share_inspections_100: Mapped[float] = mapped_column(nullable=True, comment="Доля досмотров 100%")
    views_with_sound: Mapped[int] = mapped_column(nullable=True, comment="Просмотры со звуком")

    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="campaign_statistics")


engine = create_engine("sqlite:///database.db")
sqlite_session = sessionmaker(bind=engine)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
