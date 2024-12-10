import sys
import pygame
from Board import Board

# Vars
running = True
square_size = 32
board_size = square_size * 8
scale = 3
board = Board(square_size, scale)
# dt = clock.tick(60) / 1000 Delta Time

pygame.init()
screen = pygame.display.set_mode((board_size * scale, board_size * scale))
clock = pygame.time.Clock()
pygame.display.set_caption("Multiplayer Chess")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    board.render(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()