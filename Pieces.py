from enum import Enum
import pygame


class PieceType(Enum):
    Pawn = 0
    Rook = 1
    Bishop = 2
    Knight = 3
    Queen = 4
    King = 5
    Empty = 6


class Piece:

    def __init__(self, piece : PieceType, pos : tuple[int, int], square_size : int, scale : int, color : int = 3):
        self._pos = pos
        self._piece = piece
        self._color = color
        self._scale = scale
        self._square_size = square_size
        self._image = self.image()

    def image(self):
        if self._piece == PieceType.Empty: return None
        return pygame.transform.scale(pygame.image.load("assets/" + ("White/" if self._color == 0 else "Black/") + self._piece.name + ".png"), (self._square_size * self._scale, self._square_size * self._scale))

    def set_pos(self, pos : tuple[int, int]):
        self._pos = pos

    def render(self, screen):
        if self._piece != PieceType.Empty:
            center = self._square_size / 2
            screen.blit(self._image, (self._pos[0] * self._square_size * self._scale, self._pos[1] * self._square_size * self._scale - center))

    def get_moves(self) -> list[tuple[int, int]]:
        pass

    def can_capture(self, other : "Piece") -> list[tuple[int, int]]:
        pass