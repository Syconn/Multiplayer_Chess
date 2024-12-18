# Manages GameBoard

import json
import pygame
from Pieces import Piece, PieceType


class Board:

    def __init__(self, scalar: int, flipped: bool = False):
        self._background = pygame.transform.scale(pygame.image.load("assets/Board.png"), (scalar * 8, scalar * 8))
        self._open_move = pygame.transform.scale(pygame.image.load("assets/Moves/Open.png"), (scalar, scalar))
        self._enemy_move = pygame.transform.scale(pygame.image.load("assets/Moves/Take.png"), (scalar, scalar))
        self._selector = pygame.transform.scale(pygame.image.load("assets/Selector/Selector1.png"), (scalar, scalar))
        self._scalar = scalar
        self._flipped = flipped
        self._images = self.images()
        self._selected_pos = self.clear_selection()
        self._board = self.gen_board()
        self._moves = []

    def set_flip(self, flip: bool):
        self._flipped = flip

    def images(self) -> dict[tuple[PieceType, int], pygame.Surface]:
        images = {}
        for piece in PieceType:
            if piece == PieceType.Empty:
                images[piece, 3] = None
            else:
                images[piece, 1] = pygame.transform.scale(pygame.image.load("assets/White/" + piece.name + ".png"),
                                                          (self._scalar, self._scalar))
                images[piece, 2] = pygame.transform.scale(pygame.image.load("assets/Black/" + piece.name + ".png"),
                                                          (self._scalar, self._scalar))
        return images

    def gen_board(self) -> dict[tuple[int, int], Piece]:
        board = {}
        with open("assets/game_data.json", "r") as file:
            data = json.load(file)["board"]
            for y, l in data.items():
                for x, p in enumerate(l):
                    board[x, int(y)] = self.create_piece(p, x, int(y))
        return board

    def empty_board(self) -> dict[tuple[int, int], Piece]:
        board = {}
        for x in range(8):
            for y in range(8):
                board[x, y] = Piece(self, (x, y))
        return board

    def piece(self, pos: tuple[int, int]) -> Piece:
        return self._board[pos]

    def get_eval_status(self, turn: int, other: int) -> list[Piece | list[Piece]]:
        king = None
        pieces = []
        for piece in self._board.values():
            if piece.type() == PieceType.King and piece.team(turn):
                king = piece
            elif piece.team(other):
                pieces.append(piece)
        return [king, pieces]

    def render(self, screen: pygame.Surface):
        screen.blit(self._background, (0, 0))

        for move in self._moves:
            if self.piece(self._selected_pos).take(move):
                screen.blit(self._enemy_move, self.flip(move, self._scalar))
            else:
                screen.blit(self._open_move, self.flip(move, self._scalar))

        for x in range(8):
            for y in range(8):
                self._board[x, y].render(screen, self._scalar, self.flip)

        if self._selected_pos != (-1, -1):
            screen.blit(self._selector, self.flip(self._selected_pos, self._scalar))

    def flip(self, pos: tuple[int, int], scalar: int = 1) -> tuple[int, int]:
        return (pos[0] * scalar, (7 - pos[1]) * scalar) if self._flipped else (pos[0] * scalar, pos[1] * scalar)

    def clear_selection(self) -> tuple[int, int]:
        self._moves = []
        self._selected_pos = (-1, -1)
        return self._selected_pos

    def set_selection(self, pos: tuple[int, int], turn: int, show_moves: bool):
        self.clear_selection()
        if self._selected_pos != pos: self._selected_pos = pos
        if self.piece(pos).team(turn) and show_moves:
            self._moves = self.piece(pos).get_moves()

    def moves(self) -> list[tuple[int, int]]:
        return self._moves

    def selection(self) -> tuple[int, int]:
        return self._selected_pos

    def move(self, _from: tuple[int, int], _to: tuple[int, int]) -> Piece:
        output = self._board[_to]
        self._board[_to] = self.piece(_from).set_pos(_to)
        self._board[_from] = Piece(self, _from)
        return output

    def undo(self, piece1: Piece, piece2: Piece):
        self._board[piece1.pos()] = piece1
        self._board[piece2.pos()] = piece2

    def create_piece(self, letter: str, x: int, y: int) -> Piece:
        for piece in PieceType:
            flag1 = piece.name[0] if piece != PieceType.King else "O"
            flag2 = piece.name[0].lower() if piece != PieceType.King else "o"
            if letter == "e": return Piece(self, (x, y))
            elif flag1 == letter: return Piece(self, (x, y), piece, self._images[piece, 2], 2)
            elif flag2 == letter: return Piece(self, (x, y), piece, self._images[piece, 1], 1)

    def send(self) -> bytes:
        data = ""
        for piece in self._board.values():
            if piece.type() != PieceType.Empty: data += piece.encode() + "|"
        return data.encode()

    def receive(self, received: str):
        board = self.empty_board()
        for data in filter(None, received.split("|")):
            info = data.split()
            pos = eval(info[1])
            piece = PieceType(int(info[0]))
            color = int(info[2])
            board[pos] = Piece(self, pos, piece, self._images[piece, color], color)
        self._board = board
