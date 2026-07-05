from __future__ import annotations


class CaptionService:
    def build_caption(self, outfit_title: str, aesthetic: str, board_name: str) -> tuple[str, list[str]]:
        caption = (
            f"{outfit_title} is styled for a {aesthetic.lower()} Pinterest moment. "
            f"Save this look to your {board_name.lower()} board for your next outfit refresh."
        )
        hashtags = [
            "#AmazonFashion",
            "#OutfitInspo",
            f"#{aesthetic.replace(' ', '')}",
            "#Veloura",
            "#PinterestStyle",
        ]
        return caption, hashtags

