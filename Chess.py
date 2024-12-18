# Manages Gameplay

import Board


# Todo Fix Queen Movement
class Chess:

    def __init__(self, board: Board.Board, scalar: int, my_turn: int):
        self._board = board
        self._scalar = scalar
        self._turn = 1
        self._my_turn = my_turn
        self._check = [False, False]

    def flip(self) -> bool:
        return self._my_turn == 2

    def next(self) -> int:
        return self._turn % 2 + 1

    def clicked(self, pos: tuple[int, int], button: int) -> bool:
        square = self._board.flip((pos[0] // self._scalar, pos[1] // self._scalar))
        if button == 1:
            if square in self._board.moves():
                return self.move(square)
            else:
                self._board.set_selection(square, self._turn, self._turn == self._my_turn)
        return False

    def move(self, pos: tuple[int, int]) -> bool:
        piece1 = self._board.piece(self._board.selection())
        piece2 = self._board.move(self._board.selection(), pos)
        self.eval_position()
        if self._check[self._turn - 1]:
            self._board.undo(piece1.set_pos(self._board.selection()), piece2)
            return False
        else:
            self._board.clear_selection()
            self.next_turn()
            return True

    def next_turn(self):
        self._turn = self.next()

    def eval_position(self):
        self._check[self._turn - 1] = False
        evaluation = self._board.get_eval_status(self._turn, self.next())
        for piece in evaluation[1]:
            if evaluation[0].pos() in piece.get_moves(): self._check[self._turn - 1] = True

    def eval_mate(self):
        pass
