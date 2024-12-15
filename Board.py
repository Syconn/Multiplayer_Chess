import json
import pygame
import Animator
import Pieces


class Board:

    def __init__(self, square_size : int, scale : int):
        self._background = pygame.transform.scale(pygame.image.load("assets/Board.png"), (square_size * scale * 8, square_size * scale * 8))
        self._open_move = pygame.transform.scale(pygame.image.load("assets/Moves/Open.png"), (square_size * scale, square_size * scale))
        self._enemy_move = pygame.transform.scale(pygame.image.load("assets/Moves/Take.png"), (square_size * scale, square_size * scale))
        self._square_size = square_size
        self._scale = scale
        self._selected_pos = (-1, -1)
        self._selector = Animator.ImageAnimation("assets/Selector/Selector", ".png", 4, square_size, scale, 20)
        self._board = self.gen_board()
        self._moves = []

    def piece(self, pos : tuple[int, int]) -> Pieces.Piece:
        return self._board[pos]

    def render(self, screen, dt : int):
        screen.blit(self._background, (0, 0))

        for move in self._moves:
            if self.piece(self._selected_pos).take(move): screen.blit(self._enemy_move, (move[0] * self._scale * self._square_size, move[1] * self._scale * self._square_size))
            else: screen.blit(self._open_move, (move[0] * self._scale * self._square_size, move[1] * self._scale * self._square_size))

        for x in range(8):
            for y in range(8):
                self._board[x, y].render(screen)

        if self._selected_pos != (-1, -1):
            self._selector.single_play(screen, self._selected_pos)

    def on_click(self, pos : tuple[int, int], button : int):
        square = (pos[0] // self._square_size // self._scale, pos[1] // self._square_size // self._scale)
        if button == 1:
            if square in self._moves:
                self.move(self._selected_pos, square)
                self._moves = []
                self._selected_pos = (-1, -1)
            elif self._selected_pos != square:
                self._moves = []
                self._selected_pos = square
                self._moves = self.piece(square).get_moves()
            else:
                self._selected_pos = (-1, -1)
                self._moves = []

    def gen_board(self) -> dict[tuple[int, int], Pieces.Piece]:
        board = {}
        with open("assets/game_data.json", "r") as file:
            data = json.load(file)["board"]
            for y, l in data.items():
                for x, p in enumerate(l):
                    board[x, int(y)] = self.create_piece(p, x, int(y))
        return board

    def move(self, _from : tuple[int, int], _to : tuple[int, int]):
        piece = self.piece(_from).set_pos(_to)
        self._board[_from] = Pieces.Piece(Pieces.PieceType.Empty, self, _from, self._square_size, self._scale)
        self._board[_to] = piece

    def create_piece(self, letter: str, x: int, y: int) -> Pieces.Piece:
        for piece in Pieces.PieceType:
            flag1 = piece.name[0] if piece != Pieces.PieceType.King else "O"
            flag2 = piece.name[0].lower() if piece != Pieces.PieceType.King else "o"
            if flag1 == letter: return Pieces.Piece(piece, self, (x, y), self._square_size, self._scale, 1)
            if flag2 == letter: return Pieces.Piece(piece, self, (x, y), self._square_size, self._scale, 0)
        return Pieces.Piece(Pieces.PieceType.Empty, self, (x, y), self._square_size, self._scale)