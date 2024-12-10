import pygame
import Pieces
from Pieces import Piece


def create_piece(letter : str, x : int, y : int, square_size : int, scale : int) -> Pieces.Piece:
    for piece in Pieces.PieceType:
        if piece.name[0] == letter: return Pieces.Piece(piece, (x, y), square_size, scale, 1)
        if piece.name[0].lower() == letter: return Pieces.Piece(piece, (x, y), square_size, scale, 0)
    return Pieces.Piece(Pieces.PieceType.Empty, (x, y), square_size, scale)


class Board:

    def __init__(self, square_size : int, scale : int):
        self._background = pygame.transform.scale(pygame.image.load("assets/Board.png"), (square_size * scale * 8, square_size * scale * 8))
        self._square_size = square_size
        self._scale = scale
        self._board = self.gen_board()

    def render(self, screen):
        screen.blit(self._background, (0, 0))

        for x in range(8):
            for y in range(8):
                self._board[x, y].render(screen)

    def gen_board(self) -> dict[tuple[int, int], Piece]:
        board = {}
        with open("assets/board_layout.txt", "r") as file:
            for y, text in enumerate(file):
                for x, p in enumerate(text):
                    board[x, y] = create_piece(p, x, y, self._square_size, self._scale)
        return board