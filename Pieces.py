from enum import Enum
import pygame


def in_bounds(pos: tuple[int, int]) -> bool:
    return 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7


class PieceType(Enum):
    Pawn = 0
    Rook = 1
    Bishop = 2
    Knight = 3
    Queen = 4
    King = 5
    Empty = 6


class Piece:

    def __init__(self, piece : PieceType, board, pos : tuple[int, int], square_size : int, scale : int, color : int = 3):
        self._pos = pos
        self._board = board
        self._piece = piece
        self._color = color
        self._scalar = scale * square_size
        self._square_size = square_size
        self._image = self.image()
        self._unmoved = True
    
    def piece(self, pos : tuple[int, int]) -> "Piece":
        return self._board.piece(pos)
    
    def image(self):
        if self._piece == PieceType.Empty: return None
        return pygame.transform.scale(pygame.image.load("assets/" + ("White/" if self._color == 0 else "Black/") + self._piece.name + ".png"), (self._scalar, self._scalar))

    def set_pos(self, pos : tuple[int, int]) -> "Piece":
        self._pos = pos
        self._unmoved = False
        return self

    def render(self, screen):
        if self._piece != PieceType.Empty: screen.blit(self._image, (self._pos[0] * self._scalar, self._pos[1] * self._scalar))

    def forward(self) -> int:
        if self._color == 1: return 1
        return -1

    def offset(self, offset : tuple[int, int]) -> tuple[int, int]:
        return offset[0] + self._pos[0], offset[1] + self._pos[1]

    def get_moves(self) -> list[tuple[int, int]]:
        moves = []
        if self._piece == PieceType.Pawn:
            if self.move(self.offset((0, self.forward()))): moves.append(self.offset((0, self.forward())))
            if self.take(self.offset((1, self.forward()))): moves.append(self.offset((1, self.forward())))
            if self.take(self.offset((-1, self.forward()))): moves.append(self.offset((-1, self.forward())))
            if self.move(self.offset((0, self.forward()))) and self.move(self.offset((0, self.forward() * 2))) and self._unmoved: moves.append(self.offset((0, self.forward() * 2)))
            # TODO EN PASSANT
        elif self._piece == PieceType.Knight:
            if self.move_or_take(self.offset((2, 1))): moves.append(self.offset((2, 1)))
            if self.move_or_take(self.offset((-2, 1))): moves.append(self.offset((-2, 1)))
            if self.move_or_take(self.offset((2, -1))): moves.append(self.offset((2, -1)))
            if self.move_or_take(self.offset((-2, -1))): moves.append(self.offset((-2, -1)))
            if self.move_or_take(self.offset((1, 2))): moves.append(self.offset((1, 2)))
            if self.move_or_take(self.offset((-1, 2))): moves.append(self.offset((-1, 2)))
            if self.move_or_take(self.offset((1, -2))): moves.append(self.offset((1, -2)))
            if self.move_or_take(self.offset((-1, -2))): moves.append(self.offset((-1, -2)))
        elif self._piece == PieceType.Rook:
            r = l = u = d = True
            for i in range(1, 8):
                if r and self.move_or_take(self.offset((i, 0))): moves.append(self.offset((i, 0)))
                if self.end_or_take(self.offset((i, 0))): r = False
                if l and self.move_or_take(self.offset((-i, 0))): moves.append(self.offset((-i, 0)))
                if self.end_or_take(self.offset((-i, 0))): l = False
                if u and self.move_or_take(self.offset((0, i))): moves.append(self.offset((0, i)))
                if self.end_or_take(self.offset((0, i))): u = False
                if d and self.move_or_take(self.offset((0, -i))): moves.append(self.offset((0, -i)))
                if self.end_or_take(self.offset((0, -i))): d = False
        elif self._piece == PieceType.Bishop:
            q = e = z = c = True
            for i in range(1, 8):
                if q and self.move_or_take(self.offset((i, i))): moves.append(self.offset((i, i)))
                if self.end_or_take(self.offset((i, i))): q = False
                if e and self.move_or_take(self.offset((-i, -i))): moves.append(self.offset((-i, -i)))
                if self.end_or_take(self.offset((-i, -i))): e = False
                if z and self.move_or_take(self.offset((-i, i))): moves.append(self.offset((-i, i)))
                if self.end_or_take(self.offset((-i, i))): z = False
                if c and self.move_or_take(self.offset((i, -i))): moves.append(self.offset((i, -i)))
                if self.end_or_take(self.offset((i, -i))): c = False
        elif self._piece == PieceType.Queen:
            r = l = u = d = q = e = z = c = True
            for i in range(1, 8):
                if q and self.move_or_take(self.offset((i, i))): moves.append(self.offset((i, i)))
                if self.end_or_take(self.offset((i, i))): q = False
                if e and self.move_or_take(self.offset((-i, -i))): moves.append(self.offset((-i, -i)))
                if self.end_or_take(self.offset((-i, -i))): e = False
                if z and self.move_or_take(self.offset((-i, i))): moves.append(self.offset((-i, i)))
                if self.end_or_take(self.offset((-i, i))): z = False
                if c and self.move_or_take(self.offset((i, -i))): moves.append(self.offset((i, -i)))
                if self.end_or_take(self.offset((i, -i))): c = False
                if r and self.move_or_take(self.offset((i, 0))): moves.append(self.offset((i, 0)))
                if self.end_or_take(self.offset((i, 0))): r = False
                if l and self.move_or_take(self.offset((-i, 0))): moves.append(self.offset((-i, 0)))
                if self.end_or_take(self.offset((-i, 0))): l = False
                if u and self.move_or_take(self.offset((0, i))): moves.append(self.offset((0, i)))
                if self.end_or_take(self.offset((0, i))): u = False
                if d and self.move_or_take(self.offset((0, -i))): moves.append(self.offset((0, -i)))
                if self.end_or_take(self.offset((0, -i))): d = False
        elif self._piece == PieceType.King:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if self.move_or_take(self.offset((x, y))): moves.append(self.offset((x, y)))
        return moves

    def move_or_take(self, pos : tuple[int, int]) -> bool:
        return self.take(pos) or self.move(pos)

    def move(self, pos : tuple[int, int]) -> bool:
        if not in_bounds(pos): return False
        return self.piece(pos)._piece == PieceType.Empty

    def take(self, pos : tuple[int, int]) -> bool:
        if not in_bounds(pos): return False
        other = self.piece(pos)
        return other._piece != PieceType.Empty and self._color != other._color

    def end_or_take(self, pos : tuple[int, int]) -> bool:
        if not in_bounds(pos): return False
        return self.piece(pos)._piece != PieceType.Empty