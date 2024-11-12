import time

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    create_engine,
)
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
    campaign_id: Mapped[int] = mapped_column(unique=True, nullable=False, comment="ID кампании")
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
        String(255), nullable=True, comment="Автостратегия, которая используется для кампании"
    )
    product_campaign_mode: Mapped[str] = mapped_column(
        String(255), nullable=True, comment="Режим создания и управления товарной рекламной кампанией"
    )

    search_statistics: Mapped[list["SearchStatistics"]] = relationship("SearchStatistics", back_populates="campaign")
    stencil_statistics: Mapped[list["StencilStatistics"]] = relationship("StencilStatistics", back_populates="campaign")
    banner_statistics: Mapped[list["BannerStatistics"]] = relationship("BannerStatistics", back_populates="campaign")
    video_banner_statistics: Mapped[list["VideoBannerStatistics"]] = relationship(
        "VideoBannerStatistics", back_populates="campaign"
    )


class SearchStatistics(Base):
    """Статистика по поиску"""

    __tablename__ = "search_statistics"
    __table_args__ = (UniqueConstraint("date", "sku", name="uq_search_date_sku"),)

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaign.id"), nullable=False, comment="ID кампании")
    date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    sku: Mapped[int] = mapped_column(comment="SKU")
    name: Mapped[str] = mapped_column(String(255), nullable=True, comment="Наименование")
    price: Mapped[float] = mapped_column(nullable=True, comment="Цена")
    money_spent: Mapped[float] = mapped_column(nullable=True, comment="Расход, руб, с НДС")
    order_id: Mapped[int] = mapped_column(nullable=True, comment="ID заказа")
    order_number: Mapped[int] = mapped_column(nullable=True, comment="Номер заказа")
    adv_sku: Mapped[int] = mapped_column(nullable=True, comment="Ozon ID продвигаемого товара")
    offer_id: Mapped[str] = mapped_column(String(255), nullable=True, comment="Артикул")
    quantity: Mapped[int] = mapped_column(nullable=True, comment="Количество")
    sale_price: Mapped[float] = mapped_column(nullable=True, comment="Стоимость")
    bid: Mapped[float] = mapped_column(nullable=True, comment="Ставка в процентах")
    bid_value: Mapped[float] = mapped_column(nullable=True, comment="Ставка")

    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="search_statistics")


class StencilStatistics(Base):
    """Статистика по трафаретам"""

    __tablename__ = "stencil_statistics"
    __table_args__ = (UniqueConstraint("date", "sku", name="uq_stencil_date_sku"),)

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaign.id"), nullable=False, comment="ID кампании")
    date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    sku: Mapped[int] = mapped_column(comment="SKU")
    name: Mapped[str] = mapped_column(String(255), nullable=True, comment="Наименование")
    price: Mapped[float] = mapped_column(nullable=True, comment="Цена")
    money_spent: Mapped[float] = mapped_column(nullable=True, comment="Расход, руб, с НДС")
    views: Mapped[int] = mapped_column(nullable=True, comment="Показы")
    clicks: Mapped[int] = mapped_column(nullable=True, comment="Клики")
    ctr: Mapped[float] = mapped_column(nullable=True, comment="CTR (%)")
    avg_bid: Mapped[float] = mapped_column(nullable=True, comment="Ср. цена, руб")
    orders: Mapped[int] = mapped_column(nullable=True, comment="Заказы")
    orders_money: Mapped[float] = mapped_column(nullable=True, comment="Выручка")
    models: Mapped[int] = mapped_column(nullable=True, comment="Заказы модели")
    models_money: Mapped[float] = mapped_column(nullable=True, comment="Выручка с заказов модели")

    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="stencil_statistics")


class BannerStatistics(Base):
    """Статистика по показам баннера"""

    __tablename__ = "banner_statistics"
    __table_args__ = (UniqueConstraint("campaign_id", "date", name="uq_banner_campaign_id_date"),)

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaign.id"), nullable=False, comment="ID кампании")
    date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    money_spent: Mapped[float] = mapped_column(nullable=True, comment="Расход, руб, с НДС")
    views: Mapped[int] = mapped_column(nullable=True, comment="Показы")
    clicks: Mapped[int] = mapped_column(nullable=True, comment="Клики")
    ctr: Mapped[float] = mapped_column(nullable=True, comment="CTR (%)")
    avg_bid: Mapped[float] = mapped_column(nullable=True, comment="Ср. цена, руб")
    reach: Mapped[float] = mapped_column(nullable=True, comment="Охват")
    banner: Mapped[str] = mapped_column(String(255), nullable=True, comment="Баннер")
    page_type: Mapped[str] = mapped_column(String(255), nullable=True, comment="Тип страницы")
    attributes_platform: Mapped[str] = mapped_column(String(255), nullable=True, comment="Платформа")

    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="banner_statistics")


class VideoBannerStatistics(Base):
    """Статистика по показам видеобаннера"""

    __tablename__ = "video_banner_statistics"
    __table_args__ = (UniqueConstraint("campaign_id", "date", name="uq_video_banner_campaign_id_date"),)

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaign.id"), nullable=False, comment="ID кампании")
    date: Mapped[Date] = mapped_column(Date, nullable=False, index=True)
    money_spent: Mapped[float] = mapped_column(nullable=True, comment="Расход, руб, с НДС")
    views: Mapped[int] = mapped_column(nullable=True, comment="Показы")
    clicks: Mapped[int] = mapped_column(nullable=True, comment="Клики")
    ctr: Mapped[float] = mapped_column(nullable=True, comment="CTR (%)")
    reach: Mapped[float] = mapped_column(nullable=True, comment="Охват")
    orders: Mapped[int] = mapped_column(nullable=True, comment="Заказы")
    banner_id: Mapped[int] = mapped_column(nullable=True, comment="ID баннера")
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

    campaign: Mapped["Campaign"] = relationship("Campaign", back_populates="video_banner_statistics")


engine = create_engine("sqlite:///database.db")
sqlite_session = sessionmaker(bind=engine)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
