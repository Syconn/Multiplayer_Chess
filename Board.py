import pygame as py
import Pieces

def gen_assets(color: int) -> list[py.image]:
    color = "White" if color == 0 else "Black"
    return [py.image.load("assets/" + color + "/" + p.name + ".png") for p in Pieces.PieceTypes]


class Board:

    def __init__(self, piece_size : int, board_size : int, scale : int):
        self._piece_size = piece_size
        self._board = py.transform.scale(py.image.load("assets/Board.png"), (board_size * scale, board_size * scale))
        self._white_pieces = gen_assets(0)
        self._black_pieces = gen_assets(1)

    def render(self, screen):
        screen.blit(self._board, (0, 0))