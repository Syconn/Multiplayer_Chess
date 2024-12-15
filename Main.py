import sys
import pygame
from Board import Board

# Vars
running = True
square_size = 32
board_size = square_size * 8
scale = 3
board = Board(square_size, scale)
dt = 0

pygame.init()
screen = pygame.display.set_mode((board_size * scale, board_size * scale))
clock = pygame.time.Clock()
pygame.display.set_caption("Multiplayer Chess")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        elif event.type == pygame.MOUSEBUTTONDOWN: board.on_click(event.pos, event.button)
        elif event.type == pygame.K_ESCAPE: running = False

    board.render(screen, dt)
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
sys.exit()