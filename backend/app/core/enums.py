from enum import Enum


class ProductCategory(str, Enum):
    TOPS = "tops"
    BOTTOMS = "bottoms"
    DRESSES = "dresses"
    SHOES = "shoes"
    BAGS = "bags"
    JEWELRY = "jewelry"
    ACCESSORIES = "accessories"


class OutfitStatus(str, Enum):
    DRAFT = "draft"
    GENERATED = "generated"
    PUBLISHED = "published"


class BoardStatus(str, Enum):
    QUEUED = "queued"
    GENERATED = "generated"
    FAILED = "failed"


class CampaignType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    SEASONAL = "seasonal"


class ScheduleStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"

