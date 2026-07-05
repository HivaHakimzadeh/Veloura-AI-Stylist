from pydantic import BaseModel


class AnalyticsSummary(BaseModel):
    total_products: int
    total_outfits: int
    total_boards: int
    scheduled_posts: int
    published_posts: int
    total_impressions: int
    total_clicks: int
    total_saves: int
    estimated_affiliate_earnings: float
    top_aesthetics: list[dict[str, int]]
    trending_keywords: list[str]

