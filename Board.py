# Manages GameBoard

import json
import pygame
from Pieces import Piece, PieceType


class Board:

    def __init__(self, square_size : int, scale : int):
        self._background = pygame.transform.scale(pygame.image.load("assets/Board.png"), (square_size * scale * 8, square_size * scale * 8))
        self._open_move = pygame.transform.scale(pygame.image.load("assets/Moves/Open.png"), (square_size * scale, square_size * scale))
        self._enemy_move = pygame.transform.scale(pygame.image.load("assets/Moves/Take.png"), (square_size * scale, square_size * scale))
        self._square_size = square_size
        self._scale = scale
        self._scalar = scale * square_size
        self._selected_pos = self.clear_selection()
        self._selector = pygame.transform.scale(pygame.image.load("assets/Selector/Selector1.png"), (square_size * scale, square_size * scale))
        self._board = self.gen_board()
        self._moves = []

    def piece(self, pos : tuple[int, int]) -> Piece:
        return self._board[pos]

    def get_eval_status(self, turn : int, other : int) -> list[Piece | list[Piece]]:
        king = None
        pieces = []
        for piece in self._board.values():
            if piece.type() == PieceType.King and piece.team(turn): king = piece
            elif piece.team(other): pieces.append(piece)
        return [king, pieces]

    def render(self, screen):
        screen.blit(self._background, (0, 0))

        for move in self._moves:
            if self.piece(self._selected_pos).take(move): screen.blit(self._enemy_move, (move[0] * self._scale * self._square_size, move[1] * self._scale * self._square_size))
            else: screen.blit(self._open_move, (move[0] * self._scale * self._square_size, move[1] * self._scale * self._square_size))

        for x in range(8):
            for y in range(8):
                self._board[x, y].render(screen)

        if self._selected_pos != (-1, -1):
            screen.blit(self._selector, (self._selected_pos[0] * self._scale * self._square_size, self._selected_pos[1] * self._scale * self._square_size))

    def gen_board(self) -> dict[tuple[int, int], Piece]:
        board = {}
        with open("assets/game_data.json", "r") as file:
            data = json.load(file)["board"]
            for y, l in data.items():
                for x, p in enumerate(l):
                    board[x, int(y)] = self.create_piece(p, x, int(y))
        return board

    def clicked(self, pos: tuple[int, int], button: int):
        square = (pos[0] // self._scalar, pos[1] // self._scalar)
        if button == 1:
            if square in self._moves:
                self.move(self._selected_pos, square)
                self._moves = []
                self._selected_pos = (-1, -1)

    def clear_selection(self) -> tuple[int, int]:
        self._moves = []
        self._selected_pos = (-1, -1)
        return self._selected_pos

    def set_selection(self, pos : tuple[int, int], turn : int):
        self.clear_selection()
        if self._selected_pos != pos: self._selected_pos = pos
        if self.piece(pos).team(turn):
            self._moves = self.piece(pos).get_moves()

    def moves(self) -> list[tuple[int, int]]:
        return self._moves

    def selection(self) -> tuple[int, int]:
        return self._selected_pos

    def move(self, _from : tuple[int, int], _to : tuple[int, int]) -> Piece:
        output = self._board[_to]
        self._board[_to] = self.piece(_from).set_pos(_to)
        self._board[_from] = Piece(PieceType.Empty, self, _from, self._square_size, self._scale)
        return output

    def undo(self, piece1 : Piece, piece2 : Piece):
        self._board[piece1.pos()] = piece1
        self._board[piece2.pos()] = piece2

    def create_piece(self, letter: str, x: int, y: int) -> Piece:
        for piece in PieceType:
            flag1 = piece.name[0] if piece != PieceType.King else "O"
            flag2 = piece.name[0].lower() if piece != PieceType.King else "o"
            if flag1 == letter: return Piece(piece, self, (x, y), self._square_size, self._scale, 2)
            if flag2 == letter: return Piece(piece, self, (x, y), self._square_size, self._scale, 1)
        return Piece(PieceType.Empty, self, (x, y), self._square_size, self._scale)