from pydantic import BaseModel


class AestheticBreakdown(BaseModel):
    name: str
    count: int


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
    top_aesthetics: list[AestheticBreakdown]
    trending_keywords: list[str]
