from enum import Enum
from typing import Tuple

class PieceTypes(Enum):
    Pawn = 0
    Rook = 1
    Bishop = 2
    Knight = 3
    Queen = 4
    King = 5


class Piece:

    def __init__(self, pos : Tuple[int, int]):
        self._x = pos[0]
        self._y = pos[1]

    def move_to(self, pos : Tuple[int, int]):
        self._x = pos[0]
        self._y = pos[1]

    def render(self, ):
        pass

    def get_moves(self) -> list[Tuple[int, int]]:
        pass