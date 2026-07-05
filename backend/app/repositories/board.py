from __future__ import annotations

from app.models.generated_board import GeneratedBoard
from app.repositories.base import Repository


class BoardRepository(Repository[GeneratedBoard]):
    def __init__(self) -> None:
        super().__init__(GeneratedBoard)


board_repository = BoardRepository()

