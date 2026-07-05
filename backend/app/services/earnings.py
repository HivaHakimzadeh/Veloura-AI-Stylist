from __future__ import annotations


class AffiliateEarningsService:
    def estimate(self, price_points: list[float], clicks: int, conversion_rate: float = 0.04) -> float:
        if not price_points:
            return 0.0
        avg_order = sum(price_points) / len(price_points)
        estimated_orders = clicks * conversion_rate
        return round(avg_order * estimated_orders * 0.08, 2)

