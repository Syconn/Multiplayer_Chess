import json
import pygame
import Animator
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
        self._open_move = pygame.transform.scale(pygame.image.load("assets/Moves/Open.png"), (square_size * scale * 8, square_size * scale * 8))
        self._enemy_move = pygame.transform.scale(pygame.image.load("assets/Moves/Take.png"), (square_size * scale * 8, square_size * scale * 8))
        self._square_size = square_size
        self._scale = scale
        self._selected_pos = (-1, -1)
        self._selector = Animator.ImageAnimation("assets/Selector/Selector", ".png", 4, square_size, scale, 20)
        self._board = self.gen_board()

    def render(self, screen, dt : int):
        screen.blit(self._background, (0, 0))

        for x in range(8):
            for y in range(8):
                self._board[x, y].render(screen)

        if self._selected_pos != (-1, -1):
            self._selector.single_play(screen, self._selected_pos)

    def on_click(self, pos : tuple[int, int], button : int):
        square = (pos[0] // self._square_size // self._scale, pos[1] // self._square_size // self._scale)
        if button == 1:
            if self._selected_pos != square: self._selected_pos = square
            else: self._selected_pos = (-1, -1)

    def gen_board(self) -> dict[tuple[int, int], Piece]:
        board = {}
        with open("assets/game_data.json", "r") as file:
            data = json.load(file)["board"]
            for y, l in data.items():
                for x, p in enumerate(l):
                    board[x, int(y)] = create_piece(p, x, int(y), self._square_size, self._scale)
        return board