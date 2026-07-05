from __future__ import annotations

from collections import Counter

from sqlalchemy.orm import Session

from app.core.enums import ScheduleStatus
from app.models.generated_board import GeneratedBoard
from app.models.outfit import Outfit
from app.models.pinterest import PinterestPin
from app.models.product import Product
from app.models.scheduled_post import ScheduledPost
from app.schemas.analytics import AnalyticsSummary


class AnalyticsService:
    def summary(self, db: Session) -> AnalyticsSummary:
        products = db.query(Product).all()
        outfits = db.query(Outfit).all()
        boards = db.query(GeneratedBoard).all()
        schedules = db.query(ScheduledPost).all()
        pins = db.query(PinterestPin).all()

        top_aesthetics = Counter(product.aesthetic for product in products).most_common(5)
        keywords = Counter(tag for product in products for tag in product.style_tags).most_common(8)

        return AnalyticsSummary(
            total_products=len(products),
            total_outfits=len(outfits),
            total_boards=len(boards),
            scheduled_posts=sum(1 for post in schedules if post.status == ScheduleStatus.SCHEDULED),
            published_posts=sum(1 for post in schedules if post.status == ScheduleStatus.PUBLISHED),
            total_impressions=sum(pin.impressions for pin in pins),
            total_clicks=sum(pin.clicks for pin in pins),
            total_saves=sum(pin.saves for pin in pins),
            estimated_affiliate_earnings=round(sum(post.affiliate_earnings for post in schedules), 2),
            top_aesthetics=[{"name": name, "count": count} for name, count in top_aesthetics],
            trending_keywords=[keyword for keyword, _ in keywords],
        )

