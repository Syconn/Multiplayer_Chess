import sys
import pygame as py
from Board import Board

# Vars
running = True
piece_size = 32
board_size = piece_size * 8
scale = 3
board = Board(piece_size, board_size, scale)
# dt = clock.tick(60) / 1000 Delta Time

py.init()
screen = py.display.set_mode((board_size * scale, board_size * scale))
clock = py.time.Clock()
py.display.set_caption("Multiplayer Chess")

while running:
    for event in py.event.get():
        if event.type == py.QUIT: running = False

    board.render(screen)

    py.display.flip()
    clock.tick(60)

py.quit()
sys.exit()