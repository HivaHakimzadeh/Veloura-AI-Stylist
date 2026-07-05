from __future__ import annotations

from app.models.pinterest import PinterestBoard, PinterestPin
from app.repositories.base import Repository


class PinterestBoardRepository(Repository[PinterestBoard]):
    def __init__(self) -> None:
        super().__init__(PinterestBoard)


class PinterestPinRepository(Repository[PinterestPin]):
    def __init__(self) -> None:
        super().__init__(PinterestPin)


pinterest_board_repository = PinterestBoardRepository()
pinterest_pin_repository = PinterestPinRepository()

