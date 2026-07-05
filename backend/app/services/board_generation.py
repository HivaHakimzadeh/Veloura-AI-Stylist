from __future__ import annotations

from io import BytesIO

import httpx
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy.orm import Session

from app.core.enums import BoardStatus
from app.models.outfit import Outfit
from app.repositories.board import board_repository
from app.services.storage import StorageService


class BoardGenerationService:
    WIDTH = 1000
    HEIGHT = 1500

    def __init__(self) -> None:
        self.storage_service = StorageService()

    def generate_board(self, db: Session, outfit: Outfit) -> object:
        image_bytes = self._render_board(outfit)
        storage_key, image_url = self.storage_service.save_bytes(image_bytes)
        board = board_repository.create(
            db,
            outfit_id=outfit.id,
            title=f"{outfit.title} Board",
            image_url=image_url,
            storage_key=storage_key,
            status=BoardStatus.GENERATED,
            width=self.WIDTH,
            height=self.HEIGHT,
        )
        db.commit()
        db.refresh(board)
        return board

    def _render_board(self, outfit: Outfit) -> bytes:
        canvas = Image.new("RGB", (self.WIDTH, self.HEIGHT), "#f7f1ea")
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.load_default()

        draw.rounded_rectangle((40, 40, 960, 1460), radius=40, outline="#c2a47b", width=3, fill="#fffaf5")
        draw.text((80, 90), "Veloura", fill="#7b5b3d", font=font)
        draw.text((80, 130), outfit.title, fill="#1c1917", font=font)
        draw.text((80, 160), outfit.aesthetic, fill="#7b5b3d", font=font)

        slots = [(70, 240, 470, 720), (530, 240, 930, 720), (70, 780, 470, 1260), (530, 780, 930, 1260)]
        for item, box in zip(outfit.items[:4], slots):
            image = self._load_product_image(item.product.image_url)
            image = image.resize((box[2] - box[0], box[3] - box[1]))
            canvas.paste(image, (box[0], box[1]))
            draw.text((box[0], box[3] + 12), item.product.title[:36], fill="#1c1917", font=font)
            draw.text((box[0], box[3] + 30), f"${item.product.price:.2f}", fill="#7b5b3d", font=font)

        buffer = BytesIO()
        canvas.save(buffer, format="PNG")
        return buffer.getvalue()

    def _load_product_image(self, url: str) -> Image.Image:
        try:
            response = httpx.get(url, timeout=10.0)
            response.raise_for_status()
            return Image.open(BytesIO(response.content)).convert("RGB")
        except Exception:
            placeholder = Image.new("RGB", (400, 480), "#e8ddd1")
            draw = ImageDraw.Draw(placeholder)
            draw.rectangle((40, 40, 360, 440), outline="#b08968", width=3)
            draw.text((150, 230), "Veloura", fill="#7b5b3d", font=ImageFont.load_default())
            return placeholder

